import cv2
import os
import numpy as np
import requests
import time
import threading
import face_recognition
from datetime import datetime, timedelta

# Configuration
ENABLE_UI = True  # Toggle UI on/off
DATABASE_PATH = "faces"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe6d7uhmj3o90WgZ2_tZ-J-T1GHHME4B378t2BBlJ2dk-6Xcw/formResponse"
ROLL_NUMBER_FIELD = "entry.2137375929"
UPDATE_INTERVAL = 6 * 60 * 60  # 6 hours in seconds

# Global variables
is_recognizing = False
last_update = 0
known_face_encodings = []
known_face_names = []
last_recognition_times = {}

def load_faces():
    """Load face images and prepare encodings for recognition."""
    global known_face_encodings, known_face_names
    known_face_encodings = []
    known_face_names = []
    if not os.path.exists(DATABASE_PATH):
        print(f"Error: Face database path {DATABASE_PATH} does not exist. Ensure the database is updated correctly.")
        return
    
    print("Loading known faces...")
    for image_name in os.listdir(DATABASE_PATH):
        if image_name.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(DATABASE_PATH, image_name)
            image = cv2.imread(image_path)
            if image is not None:
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                encodings = face_recognition.face_encodings(rgb_image)
                if encodings:
                    known_face_encodings.append(encodings[0])
                    # Extract name from filename (without extension)
                    name = os.path.splitext(image_name)[0]
                    known_face_names.append(name)
                    print(f"Loaded {name}")
                else:
                    print(f"No face found in {image_name}")
            else:
                print(f"Failed to load {image_name}")
    print(f"Finished loading {len(known_face_encodings)} known faces.")

def update_database():
    """Update face database by downloading files directly from GitHub repository."""
    global last_update
    try:
        # Ensure the faces directory exists
        if not os.path.exists(DATABASE_PATH):
            os.makedirs(DATABASE_PATH)
        
        # GitHub API URL to list contents of the 'faces' folder
        api_url = "https://api.github.com/repos/piyushgoel6124/attendance/contents/faces"
        headers = {"Accept": "application/vnd.github.v3+json"}
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            files = response.json()
            for file_info in files:
                if file_info['type'] == 'file' and file_info['name'].endswith(('.png', '.jpg', '.jpeg')):
                    file_url = file_info['download_url']
                    file_path = os.path.join(DATABASE_PATH, file_info['name'])
                    # Download the file
                    file_response = requests.get(file_url)
                    if file_response.status_code == 200:
                        with open(file_path, 'wb') as f:
                            f.write(file_response.content)
                        print(f"Downloaded {file_info['name']} to {file_path}")
                    else:
                        print(f"Failed to download {file_info['name']}: {file_response.status_code}")
            last_update = time.time()
            load_faces()
            print("Database updated successfully.")
        else:
            print(f"Failed to fetch file list from GitHub API: {response.status_code}")
    except Exception as e:
        print(f"Failed to update database: {e}")

def submit_attendance(roll_number):
    """Submit attendance to Google Form."""
    try:
        payload = {ROLL_NUMBER_FIELD: str(roll_number)}
        response = requests.post(FORM_URL, data=payload)
        if response.status_code == 200:
            print(f"Attendance marked for roll number {roll_number}")
        else:
            print(f"Failed to mark attendance for {roll_number}: {response.status_code}")
    except Exception as e:
        print(f"Error submitting attendance: {e}")

def database_update_thread():
    """Thread to periodically update the database."""
    global last_update
    while True:
        if time.time() - last_update > UPDATE_INTERVAL:
            update_database()
        time.sleep(60)  # Check every minute

def main():
    global is_recognizing
    # Initial database update
    update_database()
    
    # Start database update thread
    threading.Thread(target=database_update_thread, daemon=True).start()
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)  # Use 0 for default webcam, adjust if needed
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    cap.set(3, 640)
    cap.set(4, 480)
    
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read frame from webcam.")
            break
        
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(imgS)
        face_encodings = face_recognition.face_encodings(imgS, face_locations)
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                current_time = datetime.now()
                if name not in last_recognition_times or (current_time - last_recognition_times[name]).total_seconds() > 30:
                    print(f"Recognized: {name}")
                    last_recognition_times[name] = current_time
                    submit_attendance(name)  # Submit attendance on recognition
            else:
                name = "Unknown"
            
            y1, x2, y2, x1 = face_location
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        
        if ENABLE_UI:
            cv2.imshow("Attendance System", img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Quit
                break
            elif key == ord('s'):  # Start/Stop recognition
                is_recognizing = not is_recognizing
                print(f"Recognition {'started' if is_recognizing else 'stopped'}")
            elif key == ord('r'):  # Refresh database
                update_database()
                print("Manual database refresh triggered.")
        else:
            time.sleep(0.1)  # Reduce CPU usage when UI is disabled
    
    cap.release()
    if ENABLE_UI:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

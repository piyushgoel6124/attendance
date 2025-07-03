# Attendance System

A lightweight attendance system designed for Raspberry Pi 4 (2GB RAM variant) that uses a camera to capture real-time video, detect faces, match them against a database, and mark attendance. The system uploads attendance data with timestamps and roll numbers to a cloud service and updates the face database from a GitHub repository every 6 hours.

## Overview

This system uses the `face_recognition` library, which leverages dlib for face detection and encoding, to recognize individuals from a database of known faces stored in the 'faces' folder. Upon recognition, attendance is submitted to a Google Form. The system is optimized to run on minimal hardware with just power and internet access.

## Features

- Real-time face detection and recognition using a camera.
- Matches detected faces against a database of known faces (stored as `{roll_number}.png` or similar image formats).
- Marks attendance by submitting roll numbers to a Google Form.
- Updates face database from a GitHub repository every 6 hours.
- Lightweight design suitable for Raspberry Pi 4 (2GB RAM).

## Requirements

- Python 3
- Raspberry Pi 4 (2GB RAM) or similar hardware with a camera module.
- Internet access for database updates and attendance submission.

## Installation

1. **Clone the Repository** (if applicable) or copy the project files to your Raspberry Pi.
2. **Set Up Environment**:
   - Run the setup script to install dependencies:
     ```bash
     bash setup.sh
     ```
   - Alternatively, use the Python environment setup script:
     ```bash
     python3 envsetup.py
     ```
   - Or manually install requirements:
     ```bash
     pip3 install -r requirements.txt
     ```
3. **Ensure Camera is Connected** and accessible by OpenCV.

## Usage

1. **Run the Attendance System**:
   ```bash
   python3 main.py
   ```
2. **Controls** (if UI is enabled):
   - Press 'q' to quit the application.
   - Press 's' to start/stop face recognition.
   - Press 'r' to manually refresh the face database from GitHub.

## Face Database

- Faces are stored in the 'faces' directory with filenames as roll numbers (e.g., `12345.jpg`).
- The database is automatically updated every 6 hours from the GitHub repository: [https://github.com/piyushgoel6124/attendance/tree/main/faces](https://github.com/piyushgoel6124/attendance/tree/main/faces)

## Attendance Submission

- Attendance is submitted to a Google Form with the roll number upon recognition.
- A 30-second cooldown prevents multiple submissions for the same individual within a short time frame.

## Dependencies

- `opencv-python`: For camera access and image processing.
- `numpy`: For numerical operations.
- `requests`: For HTTP requests to update the database and submit attendance.
- `face_recognition`: For face detection and recognition using dlib.

## Running on Raspberry Pi

- The system is optimized for low resource usage with camera resolution set to 640x480.
- UI can be toggled off in `main.py` by setting `ENABLE_UI = False` to save resources if running headless.

## Troubleshooting

- **Camera Not Detected**: Ensure the camera module is properly connected and accessible by OpenCV. Check with a simple camera test script if needed.
- **Recognition Issues**: Verify that face images in the 'faces' directory are clear and contain detectable faces. Adjust lighting conditions if possible.
- **Dependency Installation**: If `face_recognition` fails to install, ensure `dlib` is compiled correctly for your system. On Raspberry Pi, you might need to install additional build dependencies:
  ```bash
  sudo apt-get install -y build-essential cmake libboost-all-dev
  ```

## License

[Add your license information here if applicable]

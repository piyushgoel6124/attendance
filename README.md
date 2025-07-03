# Attendance System for Raspberry Pi 4

This project implements a lightweight attendance system using face recognition on a Raspberry Pi 4 with 2GB RAM. It captures real-time video from a 1080p USB webcam, detects and recognizes faces against a database hosted on GitHub, marks attendance by submitting data to a Google Spreadsheet via a form, and updates the face database every 6 hours.

## Features
- Real-time face detection and recognition using the 'face_recognition' library.
- Attendance submission to a Google Form.
- Automatic face database updates from GitHub every 6 hours.
- Optional UI with video feed, bounding boxes (red for detected, green for recognized), and control buttons.
- Standalone operation requiring only power and internet access.

## Hardware Requirements
- Raspberry Pi 4 (2GB RAM variant)
- 1080p USB Webcam (30 FPS)
- Power supply for Raspberry Pi
- Internet connection (Wi-Fi or Ethernet)

## Software Requirements
- Raspbian OS (lightweight version recommended)
- Python 3
- OpenCV, face_recognition, dlib, and other dependencies (installed via setup script)

## Setup Instructions
1. **Prepare Raspberry Pi**:
   - Install Raspbian OS on your Raspberry Pi if not already done.
   - Connect the USB webcam to the Raspberry Pi.
   - Ensure internet connectivity is configured.

2. **Clone or Copy the Project**:
   - Copy these project files to your Raspberry Pi, or clone the repository directly if you have git installed.

3. **Run the Setup Script**:
   - Open a terminal in the directory containing these files.
   - Make the setup script executable: `chmod +x setup.sh`
   - Run the setup script with sudo privileges: `sudo ./setup.sh`
   - This script will:
     - Update the system packages.
     - Install necessary dependencies (Python, OpenCV, dlib, face_recognition, etc.).
     - Set up the attendance system to run on boot using systemd.
   - **Note**: Installing 'dlib' and 'face_recognition' on Raspberry Pi may take a long time and could fail due to memory constraints during compilation. Be prepared for potential issues, and consider using a lighter alternative if performance is a concern.

4. **Configure UI (Optional)**:
   - To enable or disable the UI, edit `main.py` and set `ENABLE_UI = True` or `ENABLE_UI = False` at the top of the file.
   - If UI is enabled, connect a display to the Raspberry Pi to view the video feed and controls.

5. **Reboot**:
   - Reboot your Raspberry Pi to ensure the service starts automatically: `sudo reboot`

## Usage
- **Automatic Start**: The system is configured to start on boot. After rebooting, it will automatically begin capturing video and processing faces if internet is available.
- **UI Controls** (if enabled):
  - **Quit**: Press 'q' to exit the application.
  - **Start/Stop Recognition**: Press 's' to toggle face recognition on/off.
  - **Refresh Database**: Press 'r' to manually update the face database from GitHub.
- **Checking Status**: Use `sudo systemctl status attendance_system.service` to check if the service is running.
- **Stopping the Service**: Use `sudo systemctl stop attendance_system.service` to temporarily stop the system.
- **Disabling Auto-Start**: Use `sudo systemctl disable attendance_system.service` to prevent the system from starting on boot.

## Troubleshooting
- **Camera Not Detected**: Ensure the USB webcam is properly connected and recognized by the Raspberry Pi. Check with `lsusb` to see if the device is listed.
- **Database Update Fails**: Verify internet connectivity. Check logs with `journalctl -u attendance_system.service` for specific errors related to git commands.
- **Attendance Submission Fails**: Ensure the Google Form URL and field ID in `main.py` are correct. Check for network issues.
- **Performance Issues**: The 'face_recognition' library is resource-intensive and may run slowly on a Raspberry Pi 4 with 2GB RAM. If the system is slow, consider disabling the UI by setting `ENABLE_UI = False` in `main.py` to reduce resource usage, or revert to a lighter face recognition method using OpenCV's LBPH (consult previous versions of the script).
- **Installation Issues with dlib/face_recognition**: Compiling 'dlib' on Raspberry Pi can fail due to memory constraints. If installation fails, consider increasing swap space temporarily or using a pre-built wheel if available for your architecture.

## Customization
- **Face Recognition Tolerance**: Adjust the tolerance value in `main.py` (line with `tolerance=0.5`) to make recognition stricter or more lenient (lower values are stricter).
- **Camera Settings**: Modify resolution or frame rate in `main.py` if needed for performance (`cap.set` lines).
- **Database Update Interval**: Change `UPDATE_INTERVAL` in `main.py` to adjust how often the database is updated from GitHub.

## Notes
- The face database is pulled from the GitHub repository: https://github.com/piyushgoel6124/attendance/tree/main/faces
- Faces should be named as `{roll_number}.png` or `{roll_number}.jpg` for the system to extract roll numbers correctly.
- Attendance data is submitted to the specified Google Form, which automatically logs timestamps.
- Due to the use of 'face_recognition', performance on Raspberry Pi 4 may be suboptimal. This library is better suited for more powerful hardware. Consider testing on a development machine before deployment.

For any issues or further customization, refer to the script comments in `main.py` or contact the developer.

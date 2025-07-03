import os
import subprocess
import sys

def setup_environment():
    """Set up the Python environment with required packages for the attendance system."""
    print("Setting up the environment for the attendance system...")
    
    # Ensure pip is up to date
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install required packages
    required_packages = [
        "opencv-python",
        "numpy",
        "requests",
        "face_recognition"
    ]
    
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}. Please install it manually.")
    
    print("Environment setup complete. All required packages have been installed.")

if __name__ == "__main__":
    setup_environment()

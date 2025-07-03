#!/bin/bash

# Script to set up the environment for the attendance system

# Update package list
sudo apt-get update

# Install Python and pip if not already installed
sudo apt-get install -y python3 python3-pip

# Install required Python packages
pip3 install opencv-python numpy requests face_recognition

# Install any additional dependencies if needed
# sudo apt-get install -y <additional-packages>

echo "Setup complete. All required packages have been installed."

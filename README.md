# GestureMR4BMS
Hand Gesture Controlled Mixed Reality for Falcon BMS

Overview
This project utilizes a webcam to recognize hand gestures and control the Mixed Reality (MR) Cover for Falcon BMS. Using MediaPipe for hand tracking and pynput for simulating keyboard inputs, this program toggles the MR Cover in response to specific hand gestures.

Features
Real-Time Hand Tracking: Utilizes MediaPipe to detect and track hand movements in real-time.
Gesture Recognition: Recognizes specific hand gestures to trigger actions.
MR Control: Toggles the MR Cover in Falcon BMS based on recognized hand gestures.
Requirements
Python 3.x
OpenCV
MediaPipe
Pynput

Installation
Clone the Repository
git clone https://github.com/solemnify2/GestureMR4BMS
cd GestureMR4BMS


Install the Required Libraries
pip install opencv-python mediapipe pynput
python GestureMR4BMS.py

Usage
Run the Script

Gesture to Toggle MR

The program recognizes an open hand gesture to toggle the MR Cover. When an open hand is detected, it simulates a keyboard input to toggle the MR Cover in Falcon BMS.

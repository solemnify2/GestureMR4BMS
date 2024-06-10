# Hand Gesture Controlled Mixed Reality for Falcon BMS

## Overview
This project utilizes a webcam to recognize hand gestures and control the Mixed Reality (MR) Cover for Falcon BMS. Using MediaPipe for hand tracking and `pynput` for simulating keyboard inputs, this program toggles the MR Cover in response to simple hand gestures.

## Features
- **Real-Time Hand Tracking**: Utilizes MediaPipe to detect and track hand movements in real-time.
- **MR Control**: Toggles the MR Cover in Falcon BMS based on recognized hand gestures.

## Requirements
- Python 3.x
- OpenCV
- MediaPipe
- Pynput

## Installation
1. **Download GestureMR4BMS.py**
[GestureMR4BMS.py
](https://github.com/solemnify2/GestureMR4BMS/blob/main/GestureMR4BMS.py)

2. **Install Python**

3. **Install the Required Python Libraries**
   ```bash
   pip install opencv-python mediapipe pynput

## Usage
1. **Run the Script before BMS launch**
   ```bash
   python GestureMR4BMS.py
   
2. **Gesture in front of the Webcam to Toggle MR within BMS VR cockpit**
- The program recognizes an open hand gesture to toggle the MR Cover. When an open hand is detected, it simulates a keyboard input to toggle the MR Cover in Falcon BMS.

## How It Works
- **Hand Tracking**: The program uses MediaPipe to track hand landmarks in real-time through the webcam.
- **MR Toggle**: When the gesture is detected, a simulated keyboard input (pressing 'shift D1') is sent to toggle the MR Cover in Falcon BMS.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.



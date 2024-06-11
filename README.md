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
1. **Download**
[GestureMR4BMS.py
](https://github.com/solemnify2/GestureMR4BMS/blob/main/GestureMR4BMS.py) from this site

2. **Install Python** You may visit [https://python.org
](https://www.python.org/) to download installation package.

4. **Install the Required Python Libraries** Open a command prompt window in Windows and enter the following:
   ```bash
   pip install opencv-python mediapipe pynput

5. **Install and adjust Web Camera:** The recommended installation position for the camera is at the top of your monitor. Angle the camera significantly downward to face below the monitor where your MFD or ICP is located.

## Usage
1. **Run the Script before BMS launch**
   ```bash
   python GestureMR4BMS.py

2. **Run Falcon BMS as usual**

3. **Gesture in front of the Webcam to Toggle MR within BMS VR cockpit:** The program recognizes an open hand gesture to toggle the MR Cover. When an open hand is detected, it simulates a keyboard input to toggle the MR Cover in Falcon BMS. 
That's all.

## Tips

1. **Camera Position** The recommended installation position for the camera is at the top of your monitor. Angle the camera significantly downward to face below the monitor where your MFD or ICP is located. When seated and reaching your hand towards the MFD, the camera should be positioned so that your hand appears in the lower half of the video feed. Using a camera recording program to check where your hand appears in the video is a good way to ensure proper installation. The current setup is configured to recognize hands only in the lower half of the video feed. The upper half of the video feed is likely occupied by your HOTAS, and hand detection is disabled in this area to avoid false positives.
   ![camera installation](https://github.com/solemnify2/GestureMR4BMS/assets/50224420/078c2136-c10b-462d-a8b5-429b905813cf)

Currently, the program is hardcoded to recognize hands only in the lower part of the camera feed. If you want to change this region, modify the source code accordingly. The following source code contains logic to check if the hand is located at 60% or more of the y-coordinate in the video feed. Change this value to a suitable one.

   ```
   if wrist.y > 0.6:
      keyboard.press('1')
      :
   ```

2. **Reverse Operation** The current method to toggle the MR cover is using the keyboard input Shift+1. This operates on a toggle basis, which means the MR cover might turn on or off in reverse if there are detection errors. If you encounter this issue, you can manually resolve it by pressing Shift+1 on your keyboard. This manual input should correct the toggle state. It would greatly help resolve this issue if the Falcon BMS team could change the MR cover toggle key to a dedicated on/off key. This would eliminate the ambiguity caused by the toggle mechanism and ensure more reliable operation.

## How It Works
- **Hand Tracking**: The program uses MediaPipe to track hand landmarks in real-time through the webcam.
- **MR Toggle**: When the gesture is detected, a simulated keyboard input (pressing 'shift D1') is sent to toggle the MR Cover in Falcon BMS.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.



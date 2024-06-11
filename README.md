# Hand Gesture Controlled Mixed Reality for Falcon BMS

## Overview
This project utilizes a webcam to recognize hand gestures and control the Mixed Reality (MR) Cover for Falcon BMS. Using MediaPipe for hand tracking and `pynput` for simulating keyboard inputs, this program toggles the MR Cover in response to simple hand gestures.

## Features
- **Real-Time Hand Tracking**: Utilizes MediaPipe to detect and track hand movements in real-time.
- **MR Control**: Toggles the MR Cover in Falcon BMS based on recognized hand gestures.

## Requirements
- none
  
## Usage
1. **Download Pre-built [Latest Release](https://github.com/solemnify2/GestureMR4BMS/releases/download/v0.0.1/GestureMR4BMS-v0.0.1.exe). There is no installation package yet.**
2. **Run downloaded GestureMR4BMS.exe before BMS launch**
   ```
   GestureMR4BMS.exe
   ```
3. **Run Falcon BMS as usual**
4. **Gesture in front of the Webcam to Toggle MR within BMS VR cockpit:** The program recognizes an open hand gesture to toggle the MR Cover. When an open hand is detected, it simulates a keyboard input to toggle the MR Cover in Falcon BMS. 
That's all.

## Tips

1. **Camera Position** The recommended installation position for the camera is at the top of your monitor. Angle the camera significantly downward to face below the monitor where your MFD or ICP is located. When seated and reaching your hand towards the MFD, the camera should be positioned so that your hand appears in the lower half of the video feed. Using a camera recording program to check where your hand appears in the video is a good way to ensure proper installation. The upper half of the video feed is likely occupied by your HOTAS, and hand detection is disabled in this area to avoid false positives.
   ![camera installation](https://github.com/solemnify2/GestureMR4BMS/assets/50224420/078c2136-c10b-462d-a8b5-429b905813cf)
Currently, the program is hardcoded to recognize hands only in the lower part of the camera feed. If you want to change this region, modify the source code accordingly. The following source code contains logic to trigger MR Cover if the hand is located at 60% or more of the y-coordinate in the video feed. Change this value to a suitable one.

   ```python
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



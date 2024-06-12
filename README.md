# Hand Gesture Controlled Mixed Reality for Falcon BMS

## Overview
This project utilizes a webcam to recognize hand gestures and control the Mixed Reality (MR) Cover for Falcon BMS. Using MediaPipe for hand tracking and `pynput` for simulating keyboard inputs, this program toggles the MR Cover in response to simple hand gestures.

## Features
- **Real-Time Hand Tracking**: Utilizes MediaPipe to detect and track hand movements in real-time.
- **MR Control**: Toggles the MR Cover in Falcon BMS based on recognized hand gestures.

## Requirements
- none
  
## Usage
1. **Download Pre-built GestureMR4BMS executable**  
   [GUI Version](https://github.com/solemnify2/GestureMR4BMS/releases/download/v0.0.4/GestureMR4BMSGUI-v0.0.4.exe)
   [Command Line Version (will be deprecated soon)](https://github.com/solemnify2/GestureMR4BMS/releases/download/v0.0.3/GestureMR4BMS-v0.0.3.exe).  
   There is no installer yet.
3. **Run downloaded executable before BMS launch**  
   - Start: Start hand detection  
   - Stop: Stop hand detection  
   - Quit: Quit this program  
   - Detection Area(Y-coordinate %): Detection area slider. Green rectangle is current area.  
   - View Webcam Feed: Toggle for viewing webcam feed, ROI and detected hand!!! 
   !([running image](https://private-user-images.githubusercontent.com/50224420/338950273-f8c0cd7e-e1be-4193-ab2f-3a4412ac820e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTgxOTI2NDYsIm5iZiI6MTcxODE5MjM0NiwicGF0aCI6Ii81MDIyNDQyMC8zMzg5NTAyNzMtZjhjMGNkN2UtZTFiZS00MTkzLWFiMmYtM2E0NDEyYWM4MjBlLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MTIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjEyVDExMzkwNlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWY0MGMwMDg2MzUwY2M3MDhkOTkyMDg2NWRlODlhZGJhNzM4MGIzYmE4ZWY3MzBlZjBjZjk4MzUxOTAyNzcxY2ImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.Ok_b3rSeiEsnPzYWqhru4G-YI8PbVAmtZ4o-Z0-wLa0))
5. **Run Falcon BMS as usual**
6. **Gesture in front of the Webcam to Toggle MR within BMS VR cockpit:** The program recognizes an open hand gesture to toggle the MR Cover. When an open hand is detected, it simulates a keyboard input to toggle the MR Cover in Falcon BMS. 
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



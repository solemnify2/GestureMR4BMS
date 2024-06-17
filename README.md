# Hand Gesture Controlled Mixed Reality for Falcon BMS

## Overview
This project utilizes a webcam to recognize hand gestures and control the Mixed Reality (MR) Cover for Falcon BMS. Using MediaPipe for hand tracking and `pynput` for simulating keyboard inputs, this program toggles the MR Cover in response to simple hand gestures.

## Features
- **Real-Time Hand Tracking**: Utilizes MediaPipe to detect and track hand movements in real-time.
- **MR Control**: Toggles the MR Cover in Falcon BMS based on recognized hand gestures.

## Info
   I have previously distributed Python scripts as executable files built using PyInstaller for those who are not familiar with Python. However, there is currently an issue where executable files built with PyInstaller are being detected as viruses by Windows Defender. I am still unsure how to resolve this issue, so I will not be distributing these generated executable files. I am sorry for any inconvenience this may cause.

## Requirements
- Python
- Python libraries: cv2 mediapipe pynput tkinter pystray
  
## Usage

1. **Install python:**
   Visit python.org or microsoft store
   
2. **Install python libraries:** Open command prompt and run following
   ```
   pip install cv2 mediapipe pynput tkinter pystray
   ```
3. **Download and Run GestureMR4BMSGUI.py script before BMS launch:** Adjust camera position and detection area. Checking **"View Webcam Feed"** will greatly help this job. Once you are satisfied, **uncheck** it to minimize unnecessary overhead caused by this program.
   - Start: Start hand detection  
   - Stop: Stop hand detection  
   - Quit: Quit this program
   - Detection Area(Y-coordinate %): Slider to adjust detection area. Green rectangle in camera feed is current area.
   - View Webcam Feed: Toggle for viewing webcam feed, ROI and detected hand!!! 
   - '_': Minimize to tray
   - 'x': Quit program

4. **Run Falcon BMS as usual**

5. **Hand Gesture in front of the Webcam to Toggle MR within BMS VR cockpit:** That's all.

## Tips

1. **Camera Position** The recommended installation position for the camera is at the top of your monitor. Angle the camera significantly downward to face below the monitor where your MFD or ICP is located. When seated and reaching your hand towards the MFD, the camera should be positioned so that your hand appears in the lower half of the video feed. Using a camera recording program to check where your hand appears in the video is a good way to ensure proper installation. The upper half of the video feed is likely occupied by your HOTAS, and hand detection is disabled in this area to avoid false positives.
    ![image](https://private-user-images.githubusercontent.com/50224420/338950273-f8c0cd7e-e1be-4193-ab2f-3a4412ac820e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTgxOTI4MjEsIm5iZiI6MTcxODE5MjUyMSwicGF0aCI6Ii81MDIyNDQyMC8zMzg5NTAyNzMtZjhjMGNkN2UtZTFiZS00MTkzLWFiMmYtM2E0NDEyYWM4MjBlLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MTIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjEyVDExNDIwMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWIyYTEwODZiZjQ0ZDYwY2M5NWNjODNkMjNjYjM4ZGQ5OTc3MDI3NWZlN2FlOGNkNmM3OGRjZDgzNWNiMjY2YTgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.uKYfvzJ3ZuWaBs0pGyeN5KV3QyrJZkfvP3kaP2bvEHI)
   
2. **Reverse Operation** The current method to toggle the MR cover is using the keyboard input Shift+1. This operates on a toggle basis, which means the MR cover might turn on or off in reverse if there are detection errors. If you encounter this issue, you can manually resolve it by pressing Shift+1 on your keyboard. It would greatly help resolve this issue if the Falcon BMS team could change the MR cover toggle key to a dedicated on/off key. This would eliminate the ambiguity caused by the toggle mechanism and ensure more reliable operation.
3. **Making executable** You can convert Python scripts into executable files using PyInstaller. Please follow the instructions below to create the executable file

- Build pyinstaller spec file first.
```
pyinstaller --onefile --noconsole GestureMR4MBSGUI.py
```
- Modify pyinstaller spec file. Please modify the mediapipe-related path in the spec file as shown below. In the example, 'solemn' is my account name on my PC. The exact path will differ for each PC, so please find the mediapipe module path in your file explorer and change it accordingly.
```
    datas=[
      ('C:\\Users\\solem\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\mediapipe\\modules', 'mediapipe\\modules'),
    ],
```
- Rebuild executable from pyinstaller spec file
```
pyinstaller GestureMR4BMSGUI.spec
```

## How It Works
- **Hand Tracking**: The program uses MediaPipe to track hand landmarks in real-time through the webcam.
- **MR Toggle**: When the gesture is detected, a simulated keyboard input (pressing 'shift D1') is sent to toggle the MR Cover in Falcon BMS.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.



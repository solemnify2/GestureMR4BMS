# Hand Gesture Controlled Mixed Reality for Falcon BMS

## Overview
This project utilizes a webcam to recognize hand gestures and control the Mixed Reality (MR) Cover for Falcon BMS. Using MediaPipe for hand tracking and `pynput` for simulating keyboard inputs, this program toggles the MR Cover in response to simple hand gestures.

## Features
- **Real-Time Hand Tracking**: Utilizes MediaPipe to detect and track hand movements in real-time.
- **MR Control**: Toggles the MR Cover in Falcon BMS based on recognized hand gestures.

## Requirements
- None
  
## Usage

1. **Download latest GestureMR4BMSGUI.exe:**  There is an issue with Windows Defender detecting my program as a virus. To avoid this, please create a folder "C:\Falcon BMS 4.37\Tools\GestureMR4BMS" and place the executable file there to avoid the warning. If Windows Defender gives a virus warning immediately after downloading, please temporarily turn off Windows Defender's virus scanning and then proceed with the download.

    [([Latest Release](https://github.com/solemnify2/GestureMR4BMS/releases/download/0.2.4/GestureMR4BMSGUI-v0.2.4.exe))](https://github.com/solemnify2/GestureMR4BMS/releases/latest)

2. **Run GestureMR4BMSGUI.exe before BMS launch:** Adjust camera position and detection area. Checking **"View Webcam Feed"** will greatly help this job. Once you are satisfied, **uncheck** it to minimize unnecessary overhead caused by this program.

   ![Running](https://github.com/solemnify2/GestureMR4BMS/assets/50224420/b5ea3ba8-19db-4203-add0-e95e1ec920ce)

   - Start &#9654; / Stop &#9632; : Start or stop hand detection  
   - Detection Area: Slider to adjust detection area. Green rectangle in camera feed is current area.
   - View Webcam Feed: Toggle for viewing webcam feed, ROI and detected hand!!! 
   - '_': Minimize to tray
   - 'x': Quit this program   
   - Show: Restore main window (tray only)
   - About: About window (tray only)
   - Quit: Quit this program (tray only)

3. **Run Falcon BMS as usual** 

4. **Hand Gesture in front of the Webcam to Toggle MR within BMS VR cockpit:** That's all.

## Tips

1. **Camera Position:** The recommended installation position for the camera is at the top of your monitor. Angle the camera significantly downward to face below the monitor where your MFD or ICP is located. When seated and reaching your hand towards the MFD, the camera should be positioned so that your hand appears in the lower half of the video feed. Using a camera recording program to check where your hand appears in the video is a good way to ensure proper installation. The upper half of the video feed is likely occupied by your HOTAS, and hand detection is disabled in this area to avoid false positives.
       
2. **Reverse Operation:** The current method to toggle the MR cover is using the keyboard input Shift+1. This operates on a toggle basis, which means the MR cover might turn on or off in reverse if there are detection errors. If you encounter this issue, you can manually resolve it by pressing Shift+1 on your keyboard. It would greatly help resolve this issue if the Falcon BMS team could change the MR cover toggle key to a dedicated on/off key. This would eliminate the ambiguity caused by the toggle mechanism and ensure more reliable operation.

3. **Running python script:** If you are concerned about Windows Defender warnings, you can run the Python script instead of using the prebuilt executable.
   - **Install python:**
   Visit python.org or microsoft store
   
   - **Install python libraries:** Open command prompt and run following
   ```
   pip install cv2 mediapipe pynput tkinter pystray
   ```
   - **Download and Run GestureMR4BMSGUI.py script:**  
     
4. **Making executable:** You can convert Python scripts into executable files using PyInstaller. Please follow the instructions below to create the executable file. However, there is currently an issue where the executable file built with PyInstaller is being detected as virus by Windows Defender. 

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



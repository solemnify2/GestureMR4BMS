# Hand Gesture Controlled Mixed Reality for Falcon BMS
# Author: Hong Yeon Kim
# Date: 2024.06.10
#

import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller
import time

# MediaPipe hands Module Initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
MR_WATERMARK = 5   # MR Cover On Watermark. 

# Keyboard Controller Initialization
keyboard = Controller()

# Webcam Initialization
cap = cv2.VideoCapture(0)
mr_cover = 0

print(f"GestureMR4BMS")
print(f"    by Hong Yeon Kim(solemnify@gmail.com)") 
print(f"")
print(f"   TIP: The recommended installation position for the camera is at the top of your monitor. Angle the camera significantly downward to face below the monitor where your MFD or ICP is located. When seated and reaching your hand towards the MFD, the camera should be positioned so that your hand appears in the lower half of the video feed. Using a camera recording program to check where your hand appears in the video is a good way to ensure proper installation. The upper half of the video feed is likely occupied by your HOTAS, and hand detection is disabled in this area to avoid false positives.")
print(f"Detecting your hands...") 
print(f"")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Slow loop to save computing resource
    time.sleep(0.1)

    # 프레임을 BGR에서 RGB로 변환
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    result = hands.process(rgb_frame)

    landmarks = 0       # the number of hands detected
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # coordinate of detected wrists
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            wrist_x, wrist_y, wrist_z = wrist.x, wrist.y, wrist.z

            # x, y, z coordinate 
            # print(f"x: {wrist_x:.2f}, y: {wrist_y:.2f}, z: {wrist_z:.2f}")
            
            # (CONFIG) Specify the region for hand detection within the video. 
            #  Hands outside this region will be ignored. 
            #  0: top of the screen, 1: bottom of the screen. 0.6 is slightly below the halfway point. 
            if wrist_y > 0.6:
                landmarks = landmarks + 1
                if mr_cover == 0:                   # Immediate MR_Cover on as soon as any hands detected
                    keyboard.press(Key.shift)       # Keycode for mapping.
                    keyboard.press('1')
                    keyboard.release('1')
                    keyboard.release(Key.shift)

                    print(f"\rHand detected!!! ", end="") 

                mr_cover = MR_WATERMARK             # high watermark immediately, when any hands detected
                break

    # If no hands detected or outside detection region
    if landmarks == 0:  
        mr_cover = max(mr_cover-1,0)    # Count-down slowly

        # MR_Cover off after some delay to prevent hand detection noise
        if mr_cover == 1:
            keyboard.press(Key.shift)
            keyboard.press('1')
            keyboard.release('1')
            keyboard.release(Key.shift)
            
            print(f"\rNo Hand detected.", end="") 

# Release resources
cap.release()
cv2.destroyAllWindows()
hands.close()

import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import pystray
import subprocess
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize keyboard controller
keyboard = Controller()

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Flags to control the loop
running = False
show_feed = False

# Variable for y-coordinate threshold
threshold_y = 0.5

MR_WATERMARK = 5   # MR Cover On Watermark
mr_cover = 0

def get_git_version():
    try:
        version = subprocess.check_output(["git", "describe", "--tags"]).strip().decode('utf-8')
    except Exception:
        version = "unknown"
    return version

# Function to toggle MR cover (replace with actual implementation)
def mr_cover_on():
    keyboard.press(Key.shift)
    keyboard.press('1')
    keyboard.release('1')
    keyboard.release(Key.shift)

def mr_cover_off():
    keyboard.press(Key.shift)
    keyboard.press('1')
    keyboard.release('1')
    keyboard.release(Key.shift)

def detect_hand():
    global running, show_feed, threshold_y, mr_cover
    
    print("detect thread start")

    while running and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Get frame dimensions
        frame_height, frame_width, _ = frame.shape

        # Process the frame and find hands
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        landmarks = 0       # the number of hands detected

        # Draw hand landmarks on the frame with increased visibility 
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Check if the whole hand is in the specified area of the screen
                hand_in_specified_area = all(landmark.y > threshold_y for landmark in hand_landmarks.landmark)
                if hand_in_specified_area:
                    landmarks = landmarks + 1
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    if mr_cover == 0:                   # Immediate MR_Cover on as soon as any hands detected
                        mr_cover_on()
                        print(f"Hand detected at x: {wrist.x:.2f}, y: {wrist.y:.2f}, z: {wrist.z:.2f}, show_feed {show_feed}")
                        
                    mr_cover = MR_WATERMARK             # high watermark immediately, when any hands detected

                    if show_feed:
                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                        )
                
        # If no hands detected or outside detection region
        if landmarks == 0: 
            mr_cover = max(mr_cover - 1,0)    # Count-down slowly

            # MR_Cover off after some delay to prevent hand detection noise
            if mr_cover == 1:
                mr_cover_off()
                print(f"No Hand detected.") 

        if show_feed:
            # Draw detection area on the frame
            cv2.rectangle(frame, (0, int(threshold_y * frame_height)), (frame_width, frame_height), (0, 255, 0), 3)

            # Update the Tkinter label with the new frame
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)

        time.sleep(0.5)  # Slow down

    print("detect thread stop")

def start_detection():
    global running
    if not running:
        running = True
        thread = threading.Thread(target=detect_hand)
        thread.start()
    else:
        messagebox.showinfo("Info", "Detection is already running")

def stop_detection():
    global running
    running = False

def create_image():
    # Generate an image to use as the icon
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), "white")
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill="black")
    return image

def on_tray_quit(icon, item):
    stop_detection()
    icon.stop()
    root.quit()  # Properly exit the Tkinter main loop

def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)

def hide_window():
    root.withdraw()
    image = create_image()
    menu = (
        pystray.MenuItem('Show', show_window),
        pystray.MenuItem('Quit', on_tray_quit)
    )
    icon = pystray.Icon("GestureMR4BMS", image, "GestureMR4BMS", menu)
    threading.Thread(target=icon.run).start()

def update_threshold(value):
    global threshold_y
    threshold_y = float(value) / 100

def update_feed():
    global show_feed
    show_feed = toggle_feed_var.get()
    
def quit_program():
    stop_detection()
    cap.release()
    cv2.destroyAllWindows()

    root.quit()

# Tkinter GUI setup
root = tk.Tk()
root.title("GestureMR4BMS")

root.protocol('WM_DELETE_WINDOW', hide_window)

# Create a frame to contain the buttons and toggle switch
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# Create buttons for the main window
start_button = tk.Button(button_frame, text="Start", command=start_detection)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="Stop", command=stop_detection)
stop_button.pack(side=tk.LEFT, padx=5)

quit_button = tk.Button(button_frame, text="Quit", command=quit_program)
quit_button.pack(side=tk.LEFT, padx=5)

button_frame.pack(side=tk.TOP, fill=tk.X)

threshold_label = tk.Label(root, text="Detection Area (Y-coordinate %):")
threshold_label.pack(pady=5)

threshold_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=update_threshold)
threshold_slider.set(threshold_y * 100)
threshold_slider.pack(pady=5)

video_label = tk.Label(root)
video_label.pack(pady=10)

toggle_feed_var = tk.BooleanVar()
toggle_feed_switch = tk.Checkbutton(root, text="View Webcam Feed", variable=toggle_feed_var, command=update_feed)
toggle_feed_switch.pack(padx=5)

version_label = tk.Label(root, text=f"Version: {get_git_version()}")
version_label.pack(side=tk.BOTTOM, pady=10)

# start_detection()

root.mainloop()

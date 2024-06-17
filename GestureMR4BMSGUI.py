import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import pystray
# import subprocess
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize keyboard controller
keyboard = Controller()

# Flags to control the loop
running = False
show_feed = False
tray_start_stop = ""

# Variable for threshold
threshold_x = 0
threshold_y = 0.5

MR_WATERMARK = 5   # MR Cover On Watermark
mr_cover = 0

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
    global toogle_feed_var
        
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

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
                hand_in_specified_area = all(landmark.x > threshold_x and landmark.x < 1 - threshold_x and landmark.y > threshold_y for landmark in hand_landmarks.landmark)
                if hand_in_specified_area:
                    landmarks = landmarks + 1
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    if mr_cover == 0:                   # Immediate MR_Cover on as soon as any hands detected
                        mr_cover_on()
                        video_label.config(text=f"Hand detected at x: {wrist.x:.2f}, y: {wrist.y:.2f}, z: {wrist.z:.2f}", image='')
                        
                    mr_cover = MR_WATERMARK             # high watermark immediately, when any hands detected

                    if show_feed:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
        # If no hands detected or outside detection region
        if landmarks == 0: 
            mr_cover = max(mr_cover - 1,0)    # Count-down slowly

            # MR_Cover off after some delay to prevent hand detection noise
            if mr_cover == 1:
                mr_cover_off()
                video_label.config(text="No hand detected", image='')

        if show_feed:
            # Draw detection area on the frame
            cv2.rectangle(frame, (0, int(threshold_y * frame_height)), (frame_width, frame_height), (0, 255, 0), 3)

            # Update the Tkinter label with the new frame
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
            
        time.sleep(0.2)  # Slow down

    cap.release()
    cv2.destroyAllWindows()

def start_detection():
    global running

    if running == False:
        running = True
        thread = threading.Thread(target=detect_hand)
        thread.start()
        
        start_stop_button.config(text="\u25A0", command=stop_detection)
        
        video_label.config(text="Detecting", image='')

def stop_detection():
    global running
    
    if running == True:
        running = False
        start_stop_button.config(text="\u25B6", command=start_detection)
        
        video_label.config(text="Stopped. Click \u25B6 to start detecting.", image='')

def create_image():
    # Generate an image to use as the icon
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), "white")
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill="black")
    return image

def on_tray_start_stop(icon, item):
    global running, tray_start_stop
    
    if running == False:
        start_detection()
        
        tray_start_stop = "\u25A0 Stop"
    else:
        stop_detection()
        
        tray_start_stop = "\u25B6 Start"

def on_tray_quit(icon, item):
    stop_detection()

    icon.stop()

    root.deiconify()
    root.quit()  # Properly exit the Tkinter main loop

def show_window(icon, item):
    icon.stop()
    
#    root.after(0, root.deiconify)
    root.deiconify()

def hide_window(event=None):
    global tray_start_stop, running
    
    if root.state() == 'withdrawn':
        return
        
    root.withdraw()
    
    image = create_image()
    
    if running == False:
        tray_start_stop = "\u25B6 Start"
    else:
        tray_start_stop = "\u25A0 Stop"

    tray_menu = pystray.Menu(
        pystray.MenuItem(lambda text: tray_start_stop, on_tray_start_stop),
        pystray.MenuItem('Show', show_window),
        pystray.MenuItem('About', show_about),
        pystray.MenuItem('Quit', on_tray_quit))
        
    icon = pystray.Icon("GestureMR4BMS", image, "GestureMR4BMS", tray_menu)
    threading.Thread(target=icon.run).start()

def update_threshold(value):
    global threshold_y
    threshold_y = float(value) / 100

def update_feed():
    global show_feed
    show_feed = toggle_feed_var.get()
    video_label.config(text="", image='')
    
def quit_program():
    stop_detection()

    root.quit()

def show_about():
    messagebox.showinfo("About", "GestureMR4BMS Version 0.1.0\n\nCopyright (C) 2024 Hong Yeon Kim\n\nFor more information, visit: https://github.com/solemnify2/GestureMR4BMS")

# Tkinter GUI setup
root = tk.Tk()
root.title(f"GestureMR4BMS")

root.protocol('WM_DELETE_WINDOW', quit_program)

root.bind("<Unmap>", hide_window)

# Style
style = ttk.Style()
style.configure("TButton", padding=2)
style.map("TButton", foreground=[('pressed', 'white'), ('active', 'blue')],
                  background=[('pressed', 'blue'), ('active', 'lightblue')])

# Create a frame to contain the buttons and toggle switch
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# Create buttons for the main window
start_stop_button = ttk.Button(button_frame, text="\u25B6", width=2, command=start_detection, style="TButton")
start_stop_button.pack(side=tk.LEFT, padx=5)

threshold_label = tk.Label(button_frame, text="Detection Area:")
threshold_label.pack(side=tk.LEFT, padx=5)

threshold_slider = tk.Scale(button_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=update_threshold, showvalue=False)
threshold_slider.set(threshold_y * 100)
threshold_slider.pack(side=tk.LEFT, padx=5)

toggle_feed_var = tk.BooleanVar()
toggle_feed_switch = tk.Checkbutton(button_frame, text="View Webcam Feed", variable=toggle_feed_var, command=update_feed)
toggle_feed_switch.pack(side=tk.LEFT, padx=5)

#about_button = ttk.Button(button_frame, text="About", width=6, command=show_about, style="TButton")
#about_button.pack(side=tk.LEFT, padx=5)

button_frame.pack(side=tk.TOP, fill=tk.X)

video_label = tk.Label(root)
video_label.pack(pady=10)

start_detection()

root.mainloop()

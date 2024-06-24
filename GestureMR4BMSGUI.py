import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import pystray
import time
import sys
import os
import winreg

# Constants
REG_PATH = r"Software\GestureMR4BMS"

def set_reg(name, value):
    try:
        registry_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, str(value))
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

def get_reg(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

class GestureMR4BMSApp:
    def __init__(self, root):
        self.root = root

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

        # Initialize keyboard controller
        self.keyboard = Controller()

        # Flags to control the loop
        self.running = False
        self.show_feed = False
        self.tray_start_stop = ""

        self.load_config()

        self.MR_HIGH_WATERMARK = 5   # MR Cover On Watermark
        self.mr_cover_watermark = 0
   
        self.label = tk.Label(root)
        self.label.pack()
        
        root.title(f"GestureMR4BMS")

        # Style
        style = ttk.Style()
        style.configure("TButton", padding=2)
        style.map("TButton", foreground=[('pressed', 'white'), ('active', 'blue')],
                          background=[('pressed', 'blue'), ('active', 'lightblue')])

        # Create a frame to contain the buttons and toggle switch
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        # Create buttons for the main window
        self.start_stop_button = ttk.Button(self.button_frame, text="\u25B6", width=2, command=self.on_start_detection, style="TButton")
        self.start_stop_button.pack(side=tk.LEFT, padx=5)

        self.threshold_label = tk.Label(self.button_frame, text="Detect:")
        self.threshold_label.pack(side=tk.LEFT, padx=5)

        # Create a StringVar to hold the value of the selected option
        self.option_var = tk.StringVar()

        # Create a Combobox with detection modes
        options = ["wrist only", "any parts of hand", "all parts of hand"]
        self.combobox = ttk.Combobox(self.button_frame, textvariable=self.option_var, values=options, state='readonly')
        self.combobox.current(self.detection_mode)  # Set the default value to the first option
        self.combobox.bind("<<ComboboxSelected>>", self.on_option_select)
        self.combobox.pack(side=tk.LEFT, padx=5)

        self.toggle_feed_var = tk.BooleanVar()
        self.toggle_feed_switch = tk.Checkbutton(self.button_frame, text="View Webcam Feed", variable=self.toggle_feed_var, command=self.on_update_feed)
        self.toggle_feed_switch.pack(side=tk.LEFT, padx=5)

        self.toggle_autostart_var = tk.BooleanVar(value=self.autostart)
        self.toggle_autostart_switch = tk.Checkbutton(self.button_frame, text="Auto Start", variable=self.toggle_autostart_var, command=self.on_update_autostart)
        self.toggle_autostart_switch.pack(side=tk.LEFT, padx=5)

        self.toggle_runmin_var = tk.BooleanVar(value=self.runmin)
        self.toggle_runmin_switch = tk.Checkbutton(self.button_frame, text="Run Minimized", variable=self.toggle_runmin_var, command=self.on_update_runmin)
        self.toggle_runmin_switch.pack(side=tk.LEFT, padx=5)

        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        # Create a frame to contain video label and the vertical slider 
        self.frame2 = tk.Frame(root)
        self.frame2.pack(padx=0)

        self.video_label = tk.Label(self.frame2)
        self.video_label.pack(side=tk.LEFT, padx=0)

        self.threshold_slider_y = tk.Scale(self.frame2, from_=0, to=100, orient=tk.VERTICAL, command=self.on_update_threshold_y, showvalue=False, length=480)
        self.threshold_slider_y.set(self.threshold_y * 100)
        self.threshold_slider_y.pack(side=tk.LEFT, padx=0)

        self.frame2.pack(side=tk.TOP, fill=tk.X)
        
        self.threshold_slider_x = tk.Scale(self.root, from_=0, to=50, orient=tk.HORIZONTAL, command=self.on_update_threshold_x, showvalue=False, length=640)
        self.threshold_slider_x.set(self.threshold_x * 100)
        self.threshold_slider_x.pack(side=tk.LEFT, pady=0)
        
    def save_config(self):
        set_reg("threshold_x", str(self.threshold_x*100))
        set_reg("threshold_y", str(self.threshold_y*100))
        set_reg("mode", str(self.detection_mode))
        set_reg("autostart", "true" if self.autostart else "false")
        set_reg("runmin", "true" if self.runmin else "false")

    def load_config(self):
        #default values
        self.threshold_x = 0
        self.threshold_y = 0.5
        self.detection_mode = 0
        self.autostart = False
        self.runmin = False
        
        value = get_reg("threshold_x")
        if value != None:
            self.threshold_x = float(value)/100
        value = get_reg("threshold_y")
        if value != None:
            self.threshold_y = float(value)/100
        value = get_reg("mode")
        if value != None:
            self.detection_mode = int(value)
        value = get_reg("autostart")
        if value != None:
            self.autostart = value.lower() in ('true', '1', 't', 'y', 'yes')
        value = get_reg("runmin")
        if value != None:
            self.runmin = value.lower() in ('true', '1', 't', 'y', 'yes')
        
    # Function to toggle MR cover (replace with actual implementation)
    def mr_cover_on(self):
        self.keyboard.press(Key.shift)
        self.keyboard.press('1')
        self.keyboard.release('1')
        self.keyboard.release(Key.shift)

    def mr_cover_off(self):
        self.keyboard.press(Key.shift)
        self.keyboard.press('1')
        self.keyboard.release('1')
        self.keyboard.release(Key.shift)

    def detect_hand(self):
        #global running, show_feed, threshold_y, mr_cover_watermark
        #global toogle_feed_var, detection_mode

        ret, frame = self.cap.read()
        if not ret:
            # messagebox.showinfo("Alert", "Failed to read camera..\nDetection stopped.")
            self.on_stop_detection()
            return

        # Get frame dimensions
        frame_height, frame_width, _ = frame.shape

        # Process the frame and find hands
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)

        landmarks = 0       # the number of hands detected

        # Draw hand landmarks on the frame with increased visibility 
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                # detectio option) Select one of the followings that you prefer
                # Opt1) Check if the whole hand is in the specified area of the screen
                if (self.detection_mode == 0 and wrist.x > self.threshold_x and wrist.x < 1 - self.threshold_x and wrist.y > self.threshold_y) or \
                   (self.detection_mode == 1 and any(landmark.x > self.threshold_x and landmark.x < 1 - self.threshold_x and landmark.y > self.threshold_y for landmark in hand_landmarks.landmark)) or \
                   (self.detection_mode == 2 and all(landmark.x > self.threshold_x and landmark.x < 1 - self.threshold_x and landmark.y > self.threshold_y for landmark in hand_landmarks.landmark)):
                    landmarks = landmarks + 1
                    if self.mr_cover_watermark == 0:                   # Immediate mr_cover_watermark on as soon as any hands detected
                        self.mr_cover_on()
                        self.video_label.config(text=f"Hand detected at x: {wrist.x:.2f}, y: {wrist.y:.2f}, z: {wrist.z:.2f}")
                        
                    self.mr_cover_watermark = self.MR_HIGH_WATERMARK             # high watermark immediately, when any hands detected

                    if self.show_feed:
                        self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
        # If no hands detected or outside detection region
        if landmarks == 0: 
            self.mr_cover_watermark = max(self.mr_cover_watermark - 1,0)    # Count-down slowly

            # mr_cover_watermark off after some delay to prevent hand detection noise
            if self.mr_cover_watermark == 1:
                self.mr_cover_off()
                self.video_label.config(text="No hand detected")

        if self.show_feed:
            # Draw detection area on the frame
            cv2.rectangle(frame, (int(self.threshold_x * frame_width), int(self.threshold_y * frame_height)), (int((1-self.threshold_x) * frame_width), frame_height), (0, 255, 0), 3)

            # Update the Tkinter label with the new frame
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            
        if self.running:
            self.root.after(200, self.detect_hand)

    def on_start_detection(self):
        if self.running == False:
            
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.running = True

                self.start_stop_button.config(text="\u25A0", command=self.on_stop_detection)
                self.update_ROI()

                self.detect_hand()
            else:
                messagebox.showinfo("Error", "Failed to open camera..")

    def on_stop_detection(self):
        if self.running == True:
            self.running = False
            
            self.update_ROI()
            self.start_stop_button.config(text="\u25B6", command=self.on_start_detection)
            
            self.cap.release()

    def create_roi_image(self, is_tray):
        # Generate an image to use as the icon
        frame_width = 640
        frame_height = 480
        status_size = 100
        image = Image.new('RGB', (frame_width, frame_height), "white")
        
        dc = ImageDraw.Draw(image)
        
        dc.rectangle((int(self.threshold_x * frame_width), int(self.threshold_y * frame_height), int((1-self.threshold_x) * frame_width), frame_height), outline="green", fill="limegreen", width=5)
        if is_tray:
            if self.running:
                dc.ellipse((frame_width/2-status_size, frame_height/2-status_size, frame_width/2+status_size, frame_height/2+status_size), fill="red")
            else:
                dc.rectangle((frame_width/2-status_size, frame_height/2-status_size, frame_width/2+status_size, frame_height/2+status_size), fill="black")
        else:
            if self.running:
                dc.text((10,10), "Detecting...", fill="red")
            else:
                dc.text((10,10), "Stopped.", fill="black")
        return image

    def update_ROI(self):
        if self.show_feed == False:
            image = self.create_roi_image(False)
            imgtk = ImageTk.PhotoImage(image=image)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

    def on_tray_start_stop(self, item):
        if self.running == False:
            self.on_start_detection()
            self.tray_start_stop = "\u25A0 Stop"
        else:
            self.on_stop_detection()
            self.tray_start_stop = "\u25B6 Start"
        
        self.icon.icon = self.create_roi_image(True)

    def on_tray_quit(self, item):
        self.on_stop_detection()

        self.icon.stop()

        self.root.deiconify()
        self.root.quit()  # Properly exit the Tkinter main loop

    def on_show_window(self, item):
        self.icon.stop()
        
        self.root.after(0, self.root.deiconify)

    def on_hide_window(self, event=None):
        # global tray_start_stop, running
        
        if self.root.state() == 'withdrawn':
            return
            
        self.root.withdraw()
        
        if self.running == False:
            self.tray_start_stop = "\u25B6 Start"
        else:
            self.tray_start_stop = "\u25A0 Stop"

        self.tray_menu = pystray.Menu(
            pystray.MenuItem(lambda text: self.tray_start_stop, self.on_tray_start_stop),
            pystray.MenuItem('Configure...', self.on_show_window),
            pystray.MenuItem('About', self.on_show_about),
            pystray.MenuItem('Quit', self.on_tray_quit))
            
        image = self.create_roi_image(True)
        self.icon = pystray.Icon("GestureMR4BMS", image, "GestureMR4BMS", self.tray_menu)
        
        threading.Thread(target=self.icon.run).start()

    def on_update_threshold_x(self, value):
        self.threshold_x = float(value) / 100
        self.save_config()
        self.update_ROI()

    def on_update_threshold_y(self, value):
        self.threshold_y = float(value) / 100
        self.save_config()
        self.update_ROI()
        
    def on_update_feed(self):
        self.show_feed = self.toggle_feed_var.get()
        
        self.update_ROI()

    def on_update_autostart(self):
        self.autostart = self.toggle_autostart_var.get()
        self.save_config()

    def on_update_runmin(self):
        self.runmin = self.toggle_runmin_var.get()
        self.save_config()

    # Function to handle the selection of an option
    def on_option_select(self, event):
        self.detection_mode = self.combobox['values'].index(self.combobox.get())
        self.save_config()
        
    def on_quit_program(self):
        self.on_stop_detection()

        app.save_config()

        print("quit")
        self.root.quit()

    def on_show_about(self):
        messagebox.showinfo("About", "GestureMR4BMS Version 0.2.3\n\nCopyright (C) 2024 Hong Yeon Kim\n\nFor more information, visit: https://github.com/solemnify2/GestureMR4BMS")

if __name__ == "__main__":
    # Tkinter GUI setup
    root = tk.Tk()

    app = GestureMR4BMSApp(root)

    root.protocol('WM_DELETE_WINDOW', app.on_quit_program)
    root.bind("<Unmap>", app.on_hide_window)
    
    if app.autostart == True:
        app.on_start_detection()

    if app.runmin == True:
        app.on_hide_window()

    root.mainloop()
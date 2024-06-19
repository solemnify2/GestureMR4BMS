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

        # Variable for threshold
        self.threshold_x = 0
        self.threshold_y = 0.5
        self.detection_mode = 0

        self.MR_WATERMARK = 5   # MR Cover On Watermark
        self.mr_cover_watermark = 0
        
        self.cap = cv2.VideoCapture(0)
        
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
        self.combobox.current(0)  # Set the default value to the first option
        self.combobox.bind("<<ComboboxSelected>>", self.on_option_select)
        self.combobox.pack(side=tk.LEFT, padx=5)

        self.mode_label = tk.Label(self.button_frame, text="witin Area:")
        self.mode_label.pack(side=tk.LEFT, padx=5)

        self.threshold_slider = tk.Scale(self.button_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.on_update_threshold, showvalue=False)
        self.threshold_slider.set(self.threshold_y * 100)
        self.threshold_slider.pack(side=tk.LEFT, padx=5)

        self.toggle_feed_var = tk.BooleanVar()
        self.toggle_feed_switch = tk.Checkbutton(self.button_frame, text="View Webcam Feed", variable=self.toggle_feed_var, command=self.on_update_feed)
        self.toggle_feed_switch.pack(side=tk.LEFT, padx=5)

        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.video_label = tk.Label(root)
        self.video_label.pack(pady=10)
            
        
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

    def detect_hand(self):
        global running, show_feed, threshold_y, mr_cover_watermark
        global toogle_feed_var, detection_mode

        ret, frame = self.cap.read()
        if not ret:
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
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                # detectio option) Select one of the followings that you prefer
                # Opt1) Check if the whole hand is in the specified area of the screen
                if (self.detection_mode == 0 and wrist.x > self.threshold_x and wrist.x < 1 - self.threshold_x and wrist.y > self.threshold_y) or \
                   (self.detection_mode == 1 and any(landmark.x > self.threshold_x and landmark.x < 1 - self.threshold_x and landmark.y > self.threshold_y for landmark in hand_landmarks.landmark)) or \
                   (self.detection_mode == 2 and all(landmark.x > self.threshold_x and landmark.x < 1 - self.threshold_x and landmark.y > self.threshold_y for landmark in hand_landmarks.landmark)):
                    landmarks = landmarks + 1
                    if self.mr_cover_watermark == 0:                   # Immediate mr_cover_watermark on as soon as any hands detected
                        mr_cover_on()
                        self.video_label.config(text=f"Hand detected at x: {wrist.x:.2f}, y: {wrist.y:.2f}, z: {wrist.z:.2f}", image='')
                        
                    self.mr_cover_watermark = MR_WATERMARK             # high watermark immediately, when any hands detected

                    if self.show_feed:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
        # If no hands detected or outside detection region
        if landmarks == 0: 
            self.mr_cover_watermark = max(self.mr_cover_watermark - 1,0)    # Count-down slowly

            # mr_cover_watermark off after some delay to prevent hand detection noise
            if self.mr_cover_watermark == 1:
                mr_cover_off()
                self.video_label.config(text="No hand detected", image='')

        if self.show_feed:
            # Draw detection area on the frame
            cv2.rectangle(frame, (0, int(self.threshold_y * frame_height)), (frame_width, frame_height), (0, 255, 0), 3)

            # Update the Tkinter label with the new frame
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            
        if self.running:
            self.root.after(20, self.detect_hand)

    def on_start_detection(self):
        if self.running == False:
            self.running = True

            self.start_stop_button.config(text="\u25A0", command=self.on_stop_detection)
            self.video_label.config(text="Detecting", image='')

            self.detect_hand()        

    def on_stop_detection(self):
        if self.running == True:
            self.running = False

            self.video_label.config(text="Stopped", image='')
            self.start_stop_button.config(text="\u25B6", command=self.on_start_detection)

    def create_image(self):
        # Generate an image to use as the icon
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), "white")
        dc = ImageDraw.Draw(image)
        dc.rectangle((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill="black")
        return image

    def on_tray_start_stop(self, item):
       
        if self.running == False:
            self.on_start_detection()
            self.tray_start_stop = "\u25A0 Stop"
        else:
            self.on_stop_detection()
            self.tray_start_stop = "\u25B6 Start"

    def on_tray_quit(self, item):
        self.on_stop_detection()

        self.icon.stop()

        self.root.deiconify()
        self.root.quit()  # Properly exit the Tkinter main loop

    def on_show_window(self, item):
        self.icon.stop()
        
        self.root.after(0, self.root.deiconify)

    def on_hide_window(self, event=None):
        global tray_start_stop, running
        
        if self.root.state() == 'withdrawn':
            return
            
        self.root.withdraw()
        
        if self.running == False:
            self.tray_start_stop = "\u25B6 Start"
        else:
            self.tray_start_stop = "\u25A0 Stop"

        self.tray_menu = pystray.Menu(
            pystray.MenuItem(lambda text: self.tray_start_stop, self.on_tray_start_stop),
            pystray.MenuItem('Show', self.on_show_window),
            pystray.MenuItem('About', self.on_show_about),
            pystray.MenuItem('Quit', self.on_tray_quit))
            
        image = self.create_image()
        self.icon = pystray.Icon("GestureMR4BMS", image, "GestureMR4BMS", self.tray_menu)
        
        threading.Thread(target=self.icon.run).start()

    def on_update_threshold(self, value):
        self.threshold_y = float(value) / 100

    def on_update_feed(self):
        self.show_feed = self.toggle_feed_var.get()
        self.video_label.config(text="", image="")

    # Function to handle the selection of an option
    def on_option_select(self, event):
        self.detection_mode = self.combobox['values'].index(self.combobox.get())
        
    def on_quit_program(self):
        self.on_stop_detection()

        print("quit")
        self.root.quit()

    def on_show_about(self):
        messagebox.showinfo("About", "GestureMR4BMS Version 0.2.0\n\nCopyright (C) 2024 Hong Yeon Kim\n\nFor more information, visit: https://github.com/solemnify2/GestureMR4BMS")

if __name__ == "__main__":
    # Tkinter GUI setup
    root = tk.Tk()

    app = GestureMR4BMSApp(root)


    root.protocol('WM_DELETE_WINDOW', app.on_quit_program)
    root.bind("<Unmap>", app.on_hide_window)

    root.mainloop()
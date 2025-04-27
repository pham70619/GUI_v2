from customtkinter import CTkLabel, CTkButton
import cv2
from PIL import Image, ImageTk

class ImageCapture:
    def __init__(self, _frame):
        self.frame = _frame

        # open webcam
        # self.cap = cv2.VideoCapture(0)
        self.create_video_label()

        

    def create_video_label(self):
        self.video_label = CTkLabel(self.frame, text="")
        self.video_label.pack(side="left",padx=20, pady=20)

        # self.capture_button = CTkButton(self.frame, text="Capture Photo", command=self.capture_photo)
        # self.capture_button.pack(padx=10, pady=10)
        self.cap = cv2.VideoCapture(0)

        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)

            img = img.resize((640, 480))

            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.configure(image=imgtk)
            self.video_label.imgtk = imgtk
        self.frame.after(20, self.update_frame)

    def capture_photo(self):
        # captrue a frame on webcam
        ret, frame = self.cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((640, 480))  # resize image

            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.configure(image=imgtk, text="")
            self.video_label.imgtk = imgtk 
        else:
            self.video_label.configure(text="Failed to capture image")

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
from customtkinter import CTkFrame
from ui.image_capture import ImageCapture
from ui.control_box import Button
from ui.process_box import Process
from ui.Result import Result
from ui.console import Console
from ui.status import Status
from ui.parameter import Parameter
import tkinter as tk



class MainWindow:
    def __init__(self, master):
        self.master = master
        self.create_layout()
        self.text_font=("Arial", 16)
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.master, font=self.text_font)

        # menu file
        file_menu = tk.Menu(menu_bar, tearoff=0, font=self.text_font)
        file_menu.add_command(label="Open",font=self.text_font , command=self.open_file)
        file_menu.add_command(label="Save",font=self.text_font , command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit",font=self.text_font, command=self.master.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Menu Edit
        edit_menu = tk.Menu(menu_bar, tearoff=0, font=self.text_font)
        edit_menu.add_command(label="Undo", font=self.text_font)
        edit_menu.add_command(label="Redo", font=self.text_font)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Menu Settings
        settings_menu = tk.Menu(menu_bar, tearoff=0, font=self.text_font)
        settings_menu.add_command(label="Parameter", font=self.text_font, command=self.parameter_set)
        settings_menu.add_command(label="Preferences", font=self.text_font)
        menu_bar.add_cascade(label="Settings", font=self.text_font, menu=settings_menu)
        self.master.configure(menu=menu_bar)

    def open_file(self):
        print("Open file clicked")

    def save_file(self):
        print("Save file clicked")

    def parameter_set(self):
        self.main_frame.destroy()
        Parameter(self.master)

    def create_layout(self):
        # main frame
        self.main_frame = CTkFrame(self.master, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        # left side frame
        self.left_frame = CTkFrame(self.main_frame, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.left_frame.pack_propagate(False)

        # right side frame
        self.right_frame = CTkFrame(self.main_frame, fg_color="transparent")
        self.right_frame.pack(side="left", fill="both", expand=True)
        self.right_frame.pack_propagate(False)

        # image frame
        self.image_frame = CTkFrame(self.left_frame, border_width=1, fg_color="transparent")
        self.image_frame.pack(side="top", padx=(5, 2.5), pady=5, fill="x")

        # control frame
        self.control_frame = CTkFrame(self.left_frame, border_width=1, fg_color="transparent")
        self.control_frame.pack(side="left", padx=(5, 2.5), pady=5, fill="both", expand=True)

        # process frame
        self.process_frame = CTkFrame(self.left_frame, border_width=1, fg_color="transparent")
        self.process_frame.pack(side="left", padx=(5, 2.5), pady=5, fill="both", expand=True)

        # result frame
        self.result_frame = CTkFrame(self.right_frame, border_width=1, fg_color="transparent")
        self.result_frame.pack(side="top", padx=(2.5, 5), pady=5, fill="both", expand=True)

        # status frame
        self.status_frame = CTkFrame(self.right_frame, border_width=1, fg_color="transparent")
        self.status_frame.pack(side="top", padx=(2.5, 5), pady=5, fill="both", expand=True)

        # console frame
        self.console_frame = CTkFrame(self.right_frame, border_width=1, fg_color="transparent")
        self.console_frame.pack(side="top", padx=(2.5, 5), pady=5, fill="both", expand=True)
        
        # button group
        Button(self.control_frame)

        # process box
        Process(self.process_frame)

        # result box
        Result(self.result_frame)

        # status box
        Status(self.status_frame)

        # console
        Console(self.console_frame)

        # image-video
        ImageCapture(self.image_frame)


from customtkinter import CTkLabel, CTkFrame
import customtkinter as ctk

current_mode = ctk.get_appearance_mode()  # Lấy mode hiện tại: "Light" hoặc "Dark"

if current_mode == "Light":
    text_color = "white"
else:
    text_color = "white"

class Result:
    def __init__(self, _frame):
        self.frame = _frame
        self.result()

    def result(self):
        self.result_info = [
            ("Ok", "green"),
            ("NG", "red"),
            ("Total", "blue"),
        ]

        for text, color in self.result_info:
            item_frame = CTkFrame(self.frame, corner_radius=10)
            item_frame.pack(side="left", padx=10, pady=5, fill="both", expand=True)

            # label
            label = CTkLabel(
                item_frame,
                text=text,
                font=("Arial", 25),
            )
            label.pack(side="top", pady=10, fill="both")

            # counter
            counter = CTkLabel(
                item_frame, 
                text="0",
                font=("Arial", 60, "bold"),  
                corner_radius=10, 
                fg_color=color,
                text_color=text_color)
            counter.pack(side="top", padx=1, pady=1, fill="both", expand=True)

            
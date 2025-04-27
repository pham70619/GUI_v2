from customtkinter import CTkLabel, CTkFrame


class Status:
    def __init__(self, _frame):
        self.frame = _frame
        self.status()

    def status(self):
        self.status_info = [
            "Ok Bin",
            "NG Bin",
        ]

        for text in self.status_info:
            item_frame = CTkFrame(self.frame, corner_radius=10)
            item_frame.pack(side="left", padx=10, pady=5, fill="both", expand=True)

            # label
            label = CTkLabel(
                item_frame,
                text=text,
                font=("Arial", 20),
                height=50,         
            )
            label.pack(side="top", pady=10)

            # counter
            counter = CTkLabel(
                item_frame, 
                text="",
                width=50, 
                height=50, 
                corner_radius=25, 
                fg_color="grey")
            counter.pack(side="top", pady=5)

            
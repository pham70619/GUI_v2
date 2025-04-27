from customtkinter import CTkTextbox
from datetime import datetime

class Console:
    def __init__(self, _frame):
        self.frame = _frame
        self.console()
        self.add_log("System Initialized...")
        self.add_log("System Initialized...")
        self.add_log("System Initialized...")
        self.add_log("System Initialized...")
        self.add_log("System Initialized...")
        self.add_log("System Initialized...")
        self.add_log("System Initialized...")
        self.add_log("System Initialized...")
        self.add_log("System Initialized...")

    def console(self):
        self.console_log = CTkTextbox(self.frame, fg_color="#3A3939", text_color="white", font=("Consolas", 12))
        self.console_log.pack(padx=10, pady=10, fill="both", expand=True)

    def add_log(self, message):
        current_time = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

        log = f"{current_time} {message}"
        self.console_log.insert("end", log + '\n')
        self.console_log.see("end")

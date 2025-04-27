from customtkinter import CTkLabel, CTkFrame

class Process:
    def __init__(self, _frame):
        self.frame = _frame

        self.process()
        self.update_process("Classification")

    def process(self):
        self.process_info = [
            "Detect",
            "Classification",
            "Finish",
        ]

        self.labels = {}  # Lưu label tên tiến trình
        self.indicators = {}  # Lưu đèn chỉ thị tiến trình

        for text in self.process_info:
            item_frame = CTkFrame(self.frame)
            item_frame.pack(padx=10, pady=5, fill="x")

            # label
            label = CTkLabel(
                item_frame,
                text=text,
                font=("Arial", 20),
                height=50, 
            )
            label.pack(side="left", padx=10, fill="x")

            # LED indicator
            indicator = CTkLabel(
                item_frame, 
                text="", 
                width=20, 
                height=20, 
                corner_radius=10, 
                fg_color="grey")
            indicator.pack(side="right", padx=(0, 10))

            self.labels[text] = label
            self.indicators[text] = indicator

    def update_process(self, current_process):
        # Khi gọi hàm này, nó sẽ set đèn tương ứng sáng
        for text, indicator in self.indicators.items():
            if text == current_process:
                indicator.configure(fg_color="green")  # Sáng đèn (màu xanh)
            else:
                indicator.configure(fg_color="grey")   # Đèn tắt
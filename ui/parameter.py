from customtkinter import CTkFrame, CTkLabel, CTkButton

class Parameter:
    def __init__(self, master):
        self.master = master
        self.build_setting_screen()

    def build_setting_screen(self):
        self.main_frame = CTkFrame(self.master, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        title = CTkLabel(self.main_frame, text="Parameter Settings", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Bạn có thể thêm các thành phần setting ở đây, ví dụ các ô nhập liệu
        exit_button = CTkButton(
            self.main_frame,
            text="Exit to Main Screen",
            font=("Arial", 16),
            command=self.exit_to_main
        )
        exit_button.pack(pady=20)

    def exit_to_main(self):

        from ui.main_window import MainWindow
        # Xóa toàn bộ widgets hiện tại
        for widget in self.master.winfo_children():
            widget.destroy()

        # Gọi lại giao diện chính MainWindow
        MainWindow(self.master)
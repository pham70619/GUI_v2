from customtkinter import CTkLabel, CTkEntry, CTkButton, CTkFrame
from logic.validator import is_valid_name


class UserForm:
    def __init__(self, master):
        self.master = master
        self.build_form()

    def build_form(self):
        entry_frame = CTkFrame(self.master, fg_color="transparent")
        entry_frame.pack(pady=(10, 0), fill="x")

        CTkLabel(self.master, text="Tên người dùng").pack(pady=5)
        self.entry = CTkEntry(self.master, placeholder_text="Nhập tên...")
        self.entry.pack(pady=5)

        self.error_label = CTkLabel(entry_frame, text="", text_color="red")
        self.error_label.pack()

        btn = CTkButton(self.master, text="Xác nhận", command=self.handle_submit)
        btn.pack(pady=5)

    def handle_submit(self):
        name = self.entry.get()
        if is_valid_name(name):
            print(f"Tên hợp lệ: {name}")

        else:
            print("Tên không hợp lệ.")
            self.error_label.configure(
                text="Tên không hợp lệ. Vui lòng nhập ít nhất 3 ký tự.",
                text_color="red",
            )

from customtkinter  import CTkLabel, CTkEntry, CTkButton, CTkFrame
from logic.auth_service import authenticate
from ui.main_window import MainWindow

class loginScreen:
    def __init__(self, master):
        self.master =master
        self.build_ui()

    def build_ui(self):
        # MainWindow(self.master)

        self.main_frame = CTkFrame(self.master, bg_color="transparent",fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)


        self.frame = CTkFrame(self.main_frame, width=250, height=260, corner_radius=15)
        # self.frame.pack(padx=20, pady=20, anchor="center")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.frame.pack_propagate(False)

        CTkLabel(self.frame, text="Login the System", font=("Arial", 20, "bold")).pack(padx=20, pady=(10,20))

        # username input box
        # CTkLabel(self.frame, text="Username").pack(anchor="w", padx=10)
        self.username_entry = CTkEntry(self.frame, placeholder_text="enter username", border_width=0)
        self.username_entry.pack(padx=30, pady=(0,10), fill="x")

        # password input box
        # CTkLabel(self.frame, text="Password").pack(anchor="w", padx=10)
        self.password_entry = CTkEntry(self.frame, placeholder_text="enter password", border_width=0, show="*")
        self.password_entry.pack(padx=30, pady=(0,10), fill="x")

        self.error_label = CTkLabel(self.frame, text="", text_color="red", wraplength=200)
        self.error_label.pack(anchor="center", padx=10, fill="x")

        # login btn
        CTkButton(self.frame, text="Login", font=("Arial", 20), command=self.login).pack(side="bottom", padx=10, pady=20)

        # enter key event
        self.master.bind("<Return>", lambda event: self.login())


        self.username_entry.insert(0, "admin")
        self.password_entry.insert(0, "admin")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if authenticate(username, password):
            self.error_label.configure(text="login successful!", text_color="green")

            # delay 0.5s before destroy login screen
            self.master.after(10,self.destroy_login_screen)
            
        else:
            self.error_label.configure(text="Username or password invalid!, pls try again!.")


    def destroy_login_screen(self):
        self.main_frame.destroy()
        MainWindow(self.master)
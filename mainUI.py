# from ui.main_window import MainWindow
from ui.login_screen import loginScreen
import customtkinter as ctk

ctk.set_appearance_mode("light")  #"light" or "dark"
ctk.set_default_color_theme("green") 

app = ctk.CTk()
app.geometry("800x500")
app.title("My Ctk App")
app.resizable(width=True, height=True)

loginScreen(app)

app.mainloop()
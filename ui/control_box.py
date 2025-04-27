from customtkinter import CTkButton
import serial
import time

class Button:
    def __init__(self, _frame):
        self.frame = _frame

        try:
            self.arduino = serial.Serial(port="COM5", baudrate=9600, timeout=1)
            time.sleep(2)
            print("Aduino connected successful.")
        except Exception as e:
            print(f"Failed to connect Arduino: {e}")
            self.arduino = None

        self.create_buttons()

    def create_buttons(self):
        buttons_info = [
            ("Home", self.Home),
            ("Start", self.Start),
            ("Cycle", self.Cycle),
            ("Stop", self.Stop),
            ("Emergency", self.Emergency)
        ]

        self.buttons = {}  

        for text, command in buttons_info:
            btn = CTkButton(
                self.frame,
                text=text,
                font=("Arial", 20),
                height=50,
                command=command 
            )
            btn.pack(padx=10, pady=10, fill="x")

            self.buttons[text] = btn  

        # button is desable for default
        self.buttons["Start"].configure(state="disabled")
        self.buttons["Cycle"].configure(state="disabled")
        self.buttons["Stop"].configure(state="disabled")
        self.buttons["Emergency"].configure(state="disabled")

    # send String to arduino function
    def send_command(self, message):
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.write((message + "\n").encode())
                print(f"Sented to Arduino: {message}")
                return True
            except Exception as e:
                print(f"Failed to send command: {e}")
                return False
        else:
            print("Arduino not connected!, Pls connect to arduino first!")
            return False

    def Start(self):
        self.send_command("START")

    def Cycle(self):
        self.send_command("Cycle")

    def Stop(self):
        self.send_command("STOP")


    def Home(self):
        success = self.send_command("HOME")

        if success:
            # enable other button
            self.buttons["Start"].configure(state="normal")
            self.buttons["Stop"].configure(state="normal")
            self.buttons["Emergency"].configure(state="normal")
            print("System ready after Home!")
        else:
            print("Faild to return home point")

    def Emergency(self):
        self.send_command("EMG")


    # disconnect to arduino
    def __del__(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            print("Arduino disconnected!.")


import tkinter as tk
from tkinter import font
from tkinter import Button
from tkinter import Label
from tkinter import *
import serial
import time



#視窗設定
window = tk.Tk()
window.title("classifier")
window.geometry("750x480")

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=1)
time.sleep(2)

main_frame = tk.Frame(window, bg= "#83A6CE")
main_frame.pack(fill= "both", expand=True)

#建立字框架(左跟右)
left_frame = tk.Frame(main_frame)
left_frame.grid(padx=(10,0), pady=(5,10), row=0, column=0, sticky="nsew")

right_frame = tk.Frame(main_frame)
right_frame.grid(padx=(0,10), pady=(5,10),row=0, column=1, sticky="nsew")




#建立label frame=======================================================

#建立流程的label_frame
process_label_frame = LabelFrame(left_frame, text="Process", background="#83A6CE")
process_label_frame.grid(row = 1, column = 1, sticky = "nsew")

#建立控制按鈕label_frame
control_label_frame = LabelFrame(left_frame, text="Control", background="#83A6CE")
control_label_frame.grid(row=1, column=0, sticky="nsew")

#建立影像label_frame
image_label_frame = LabelFrame(left_frame, text="Image", background="#83A6CE")
image_label_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

#建立結果_label_frame
result_label_frame = LabelFrame(right_frame, text="Result", background="#83A6CE")
result_label_frame.pack(fill="both",expand=True)

#建立庫存狀態label frame
status_label_frame = tk.LabelFrame(result_label_frame, text="Status",  background="#83A6CE")
status_label_frame.grid(row=2, rowspan=2, column=0, columnspan= 3, padx=10, pady=10, sticky="nsew")



#格子分割============================================================

#主框架分割
main_frame.grid_columnconfigure((0, 1), weight=1)
main_frame.grid_rowconfigure((0), weight=1)

#左框架分割
left_frame.grid_columnconfigure((0, 1), weight=1)
left_frame.grid_rowconfigure((0, 1), weight=1)

#右框架分割
right_frame.grid_columnconfigure((0, 1), weight=1)
right_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

#控制label_frame 分割
control_label_frame.grid_columnconfigure((0), weight=1)
control_label_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

#流程label_frame 分割
process_label_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
process_label_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

#結果label_frame 分割
result_label_frame.grid_columnconfigure((0, 1, 2), weight=1) #三列
result_label_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1) #六行

#庫存狀態label frame 分割
status_label_frame.grid_columnconfigure((0, 1), weight=1) #兩列
status_label_frame.grid_rowconfigure((0, 1), weight=1) #一行

# #start按鈕函數
def send_start():
     arduino.write(b'START\n')  # 傳送 start 指令
     print("已傳送指令：start")
    
     # 可選：顯示 Arduino 回傳的資料
     response = arduino.readline().decode().strip()
     print("Arduino 回應：", response)
def send_home():
    arduino.write(b'HOME\n')
    print("已送出指令 HOME")

    response = arduino.readline().decode().strip()
    print("Arduino 回應:", response)
#Control
#按鍵建立函數================================================================
#字體設定
button_text_style = font.Font(family="Arial", size=12, weight="normal")

start_button = Button(control_label_frame, text="Start", command=send_start, font= button_text_style)
start_button.grid(padx=10, pady= 10, row=0, column=0, sticky="nsew")

stop_button = Button(control_label_frame, text="Stop", command="None", font= button_text_style)
stop_button.grid(padx=10, pady= 10, row=1, column=0, sticky="nsew")

emergency_button = Button(control_label_frame, text="Emergency", command="None", font= button_text_style)
emergency_button.grid(padx=10, pady= 10, row=2, column=0, sticky="nsew")

home_button = Button(control_label_frame, text="home", command=send_home, font= button_text_style)
home_button.grid(padx=10, pady= 10, row=3, column=0, sticky="nsew")


#Process
#流程=====================================================================
#字體設定
text_style = font.Font(family="Arial", size=12, weight="normal")

steps = ["Moving", "Detection", "Classification", "Finish"]

#建立流程之label
for i, step in enumerate(steps):  # 4 step
    # Đèn báo (trái)指示燈 (左)
    light = Label(process_label_frame, bg="white")
    light.grid(row=i, column=0, padx=25, pady=25, sticky="nsew")

    # Step label
    step_label = tk.Label(process_label_frame,padx=20, text=step, font=text_style, anchor="w")
    step_label.grid(row=i, column=1, columnspan=5, padx=15, pady=15, sticky="nsew")

#Result
#建立結果label================================================================
#字體設定
label_text_style = font.Font(family="Arial", size=18, weight="normal")
result_text_style = font.Font(family="Arial", size=60, weight="normal")

results = ["OK", "NG", "Total"]
background_color = ["#4CE461", "#E44C5E", "#4C9BE4"]

for i, result in enumerate(results):
    #label
    result_label = Label(result_label_frame, text=result,background="#83A6CE", font=label_text_style)
    result_label.grid(row=0, column=i, padx=25, pady=25, sticky="s")

    #result
    for i, color in enumerate(background_color):
        result = Label(result_label_frame, text="0", background=color, font=result_text_style, fg= "white")
        result.grid(row=1, column=i, padx=10, pady=10, sticky="nsew")


#Status=======================================================================
#字體設定
status_text_style = font.Font(family="Arial", size=16, weight="normal")


status = ["OK Bin", "NG Bin"]

for i, label in enumerate(status):
    #label
    status_label = Label(status_label_frame, text = label, font=status_text_style)
    status_label.grid(row=1, column=i)

    # Đèn báo hình tròn (Canvas)圓形指示燈（畫布）
    status_light = Canvas(status_label_frame, width=50, height=50, bg="#83A6CE", highlightthickness=0)
    status_light.grid(row=0, column=i, padx=10, pady=10)

    # Vẽ hình tròn
    status_light.create_oval(2, 2, 48, 48, fill="white", outline="lightgray")

    # #滿像指示燈
    # status_light = Label(status_label_frame)
    # status_light.grid(row=0, column=i)





#Console======================================================================
#建立 console log label frame
console_frame = tk.LabelFrame(result_label_frame, text="Console Log", background="#83A6CE")
console_frame.grid(row=4, rowspan=2, column=0, columnspan=3,  padx=10, pady=10, sticky="nsew")

# # Tạo Text widget cho console log 為控制台日誌建立文字小工具
console_log = tk.Text(console_frame, wrap=tk.WORD, state="normal", bg="white",height=1.5)
console_log.pack(fill="both", expand=True, padx=5, pady=5)


#尺寸鎖定=====================================================================
control_label_frame.grid_propagate(False)
process_label_frame.grid_propagate(False)
result_label_frame.grid_propagate(False)
console_frame.grid_propagate(False)


# # ctrl + /

window.mainloop()
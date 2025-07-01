import tkinter as tk
from tkinter import font
from tkinter import Button
from tkinter import Label
from tkinter import *
import serial
import time
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO
from datetime import datetime



#視窗設定
window = tk.Tk()
window.title("classifier")
window.geometry("750x480")

paperTube = YOLO("best.pt")

# 轉盤跟夾抓控制板

arduino1 = None
arduino2 = None
# global variable
ok_count = 0
ng_count = 0
total_count = 0

ok_var = tk.StringVar(value="0")
ng_var = tk.StringVar(value="0")
total_var = tk.StringVar(value="0")

# 
detect_buffer = []
process_bufer = []
status_lights = []


# 定義影像尺寸
cap = cv2.VideoCapture(1)
time.sleep(1)
# cap.set(3, 160)
# cap.set(4, 120)


def update_status_light(result):
    # result = "OK" 或 "NG"
    if result == "OK":
        status_lights[0][0].itemconfig(status_lights[0][1], fill="green")
        status_lights[1][0].itemconfig(status_lights[1][1], fill="white")
    elif result == "NG":
        status_lights[0][0].itemconfig(status_lights[0][1], fill="white")
        status_lights[1][0].itemconfig(status_lights[1][1], fill="red")

def capture_image(command = None, target = None):
    global ok_count, ng_count, total_count, detect_buffer
    # Reset LED
    for canvas, cid in status_lights:
        canvas.itemconfig(cid, fill="white")

    

    ret, frame = cap.read()
    if ret:
        if not cap.isOpened():
            add_log("Failed to connect to camera!", level="ERROR")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"saved image: {filename}")

        results = paperTube.predict(source=filename, save=True, project="results", name=timestamp, save_txt=True)
        print(f"image saved to: results/{timestamp}/")

        result = results[0]
        img_with_boxes = result.plot()

        # convert to RGB color
        img_rgb = cv2.cvtColor(img_with_boxes, cv2.COLOR_BGR2RGB)
        
        img_pil = Image.fromarray(img_rgb)
        img_pil.thumbnail((480, 360), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_pil)

        # display on UI
        image_label.config(image=img_tk)
        image_label.image = img_tk

        # result handle
        names = result.names
        classes = result.boxes.cls.tolist()
        ng_detected = any(names[int(c)].upper().startswith("NG") for c in classes)

        # store into detect_buffer
        detect_buffer.append("NG" if ng_detected else "OK")
        print(f"[Detect] {detect_buffer[-1]}")

         # if has 2 image
        if len(detect_buffer) == 2:
            if "NG" in detect_buffer:
                ng_count += 1
                result_final = "NG"
            else:
                ok_count += 1
                result_final = "OK"

            total_count += 1
            detect_buffer = []  # Reset after 2 picture

            # Update UI
            ok_var.set(str(ok_count))
            ng_var.set(str(ng_count))
            total_var.set(str(total_count))

            print(f"[Result] FINAL after 2 captures: {result_final}")
            update_status_light(result_final)
            add_log(f"Detect result: {result_final}", level="INFO")
            
            # 下發最終結果
            send_command(arduino1, f"DETECT-{result_final}")
    
    # 下發命令給 arduino1 的轉盤
    if command and target:
        send_command(target, command)



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

#建立影像label_frame)
image_label_frame = LabelFrame(left_frame, text="Image", background="#83A6CE")
image_label_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

#建立結果_label_frame
result_label_frame = LabelFrame(right_frame, text="Result", background="#83A6CE")
result_label_frame.pack(fill="both",expand=True)

#建立庫存狀態label frame
status_label_frame = tk.LabelFrame(result_label_frame, text="Status",  background="#83A6CE")
status_label_frame.grid(row=2, rowspan=2, column=0, columnspan= 3, padx=10, pady=10, sticky="nsew")

image_label_frame.grid_propagate(False)
# 影像顯示的 Label
image_label = Label(image_label_frame, width=480, height=360, bg="#83A6CE", borderwidth=0, highlightthickness=0)
image_label.place(x=0, y=0)

#Console======================================================================
#建立 console log label frame
console_frame = tk.LabelFrame(result_label_frame, text="Console Log", background="#83A6CE")
console_frame.grid(row=4, rowspan=2, column=0, columnspan=3,  padx=10, pady=10, sticky="nsew")

# # Tạo Text widget cho console log 為控制台日誌建立文字小工具
console_log = tk.Text(console_frame, wrap=tk.WORD, state="normal", bg="white",height=1.5)
console_log.pack(fill="both", expand=True, padx=5, pady=5)


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

# level : INFO; ERROR; WARNING
def add_log(message, level="INFO"):
    console_log.config(state="normal")

    timestamp = datetime.now().strftime("%H:%M:%S")
    tag = level.upper()

    log_line = f"[{timestamp}] [{tag}] {message}\n"
    console_log.insert("end", log_line, tag)
    console_log.see("end")
    console_log.config(state="disabled")

# 下發命函數
def send_command(target, command):
    # 支援target 是個 List
    targets = target if isinstance(target, list) else [target]

    for arduino in targets:
        if arduino:
            try:
                arduino.write((command + '\n').encode())
                add_log(f"已傳送指令：{command} 給 {arduino.port}", level="INFO")

            except Exception as e:
                add_log(f"[{arduino.port}] 發送 {command} 指令時出錯: {e}", level="ERROR")
        else:
            add_log(f"目標 Arduino 尚未連接，無法發送 {command} 指令", level="ERROR")


#讀取arduino 回傳的訊息
def read_arduino():
    # arduino 1
    if arduino1 and arduino1.in_waiting > 0:
        try:
            response = arduino1.readline().decode().strip()
            print(f"[Arduino 1] 收到訊息：{response}")

            # 處理回傳的訊息
            if response.upper() == "TURN OVER":
                capture_image()
            elif response.upper() == "CLAMP-OK":
             update_process_light(2)
             send_command(arduino2, "OK")
            elif response.upper() == "CLAMP-NG":
             update_process_light(2)
             send_command(arduino2, "NG")
       
        except Exception as e:
            add_log(f"讀取 Arduino1 時發生錯誤: {e}", level="ERROR")

    # arduino 2
    if arduino2 and arduino2.in_waiting > 0:
        try:
            response = arduino2.readline().decode().strip()
            print(f"[Arduino 2] 收到訊息：{response}")

            # 處理回傳的訊息
            if response.upper() == "DETECT":
                capture_image(command="TURN", target=arduino1)
            elif response.upper() == "分類結束":
             update_process_light(3)  # 亮 Finish
             send_command(arduino1, "CLIP_OPEN") 

        except Exception as e:
            add_log(f"讀取 Arduino2 時發生錯誤: {e}", level="ERROR")
    
    window.after(100, read_arduino)

#寫入txt黨
def on_closing():
    # 儲存統計數據到包含 timestamp 的檔名
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Detection_statistics-{timestamp}.txt"
        with open(filename, "w") as f:
            f.write(f"統計時間：{timestamp}\n")
            f.write(f"OK 數量：{ok_count}\n")
            f.write(f"NG 數量：{ng_count}\n")
            f.write(f"Total 數量：{total_count}\n")
        add_log(f"成功將統計資料寫入 {filename}", level="INFO")
    except Exception as e:
        add_log(f"寫入統計檔案時發生錯誤: {e}", level="ERROR")



# 視窗關閉前處理
def on_closing():
    # 中斷連線到arduino1
    if arduino1:
        try:
            arduino1.close()
            add_log("已關閉 Arduino1", level="INFO")
        except Exception as e:
            add_log(f"關閉 Arduino1 時發生錯誤: {e}", level="ERROR")

    # 中斷連線到arduino2
    if arduino2:
        try:
            arduino2.close()
            add_log("已關閉 Arduino2", level="INFO")
        except Exception as e:
            add_log(f"關閉 Arduino2 時發生錯誤: {e}", level="ERROR")

    # 中斷攝影機連線
    if cap and cap.isOpened():
        cap.release()
        add_log("已關閉攝影機", level="INFO")

    # 關閉視窗
    window.destroy()

# 指示燈函數
def update_process_light(active_index):
    for i, light in enumerate(process_lights):
        if i == active_index:
            light.config(bg="green")
        else:
            light.config(bg="white")


#Control
#按鍵建立函數================================================================
#字體設定
button_text_style = font.Font(family="Arial", size=12, weight="normal")

start_button = Button(control_label_frame, text="Start", command=lambda:[update_process_light(0), send_command(arduino2, "START")], font= button_text_style)
start_button.grid(padx=10, pady= 10, row=0, column=0, sticky="nsew")

stop_button = Button(control_label_frame, text="Stop", command="None", font= button_text_style)
stop_button.grid(padx=10, pady= 10, row=1, column=0, sticky="nsew")

emergency_button = Button(control_label_frame, text="Emergency", command="None", font= button_text_style)
emergency_button.grid(padx=10, pady= 10, row=2, column=0, sticky="nsew")

home_button = Button(control_label_frame, text="home", command=lambda:[update_process_light(0), send_command([arduino1, arduino2], "HOME")], font= button_text_style)
home_button.grid(padx=10, pady= 10, row=3, column=0, sticky="nsew")


#Process
#流程=====================================================================
#字體設定
text_style = font.Font(family="Arial", size=12, weight="normal")

steps = ["Moving", "Detection", "Classification", "Finish"]

process_lights = []

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
count_vars = [ok_var, ng_var, total_var]

# create label
for i, result in enumerate(results):
    result_label = Label(result_label_frame, text=result, background="#83A6CE", font=label_text_style)
    result_label.grid(row=0, column=i, padx=25, pady=25, sticky="s")

# create result
for i, (color, var) in enumerate(zip(background_color, count_vars)):
    value_label = Label(result_label_frame, textvariable=var, background=color, font=result_text_style, fg="white")
    value_label.grid(row=1, column=i, padx=10, pady=10, sticky="nsew")


#Status=======================================================================
#字體設定
status_text_style = font.Font(family="Arial", size=16, weight="normal")

status = ["OK Bin", "NG Bin"]

for i, label in enumerate(status):
    status_label = Label(status_label_frame, text=label, font=status_text_style)
    status_label.grid(row=1, column=i)

    status_light = Canvas(status_label_frame, width=50, height=50, bg="#83A6CE", highlightthickness=0)
    status_light.grid(row=0, column=i, padx=10, pady=10)

    # Vẽ hình tròn và lưu lại ID
    circle_id = status_light.create_oval(2, 2, 48, 48, fill="white", outline="lightgray")
    status_lights.append((status_light, circle_id))



try:
    arduino1 = serial.Serial(port='/dev/ttyACM1', baudrate=115200, timeout=1)
    time.sleep(2)
    add_log("已連接 Arduino1（轉盤與夾爪控制）", level="INFO")
except Exception as e:
    add_log(f"無法連接 Arduino1: {e}", level="ERROR")

try:
    arduino2 = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    time.sleep(2)
    add_log("已連接 Arduino2（主機構控制）", level="INFO")
except Exception as e:
    add_log(f"無法連接 Arduino2: {e}", level="ERROR")





#尺寸鎖定=====================================================================
control_label_frame.grid_propagate(False)
process_label_frame.grid_propagate(False)
result_label_frame.grid_propagate(False)
console_frame.grid_propagate(False)


# 啟動讀取arduino 回傳訊息的函數
window.after(100, read_arduino) #每100 豪秒讀一次
# 註冊關閉前處理的函數
window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
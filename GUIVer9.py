import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import cv2
import numpy as np
import threading
from ultralytics import YOLO
from tkinter import font
import serial 
import time
from queue import Queue
from datetime import datetime
import os 
import cvzone

# Cấu hình mô hình và camera
cap = cv2.VideoCapture(0)
cap.set(3, 160)  # Giảm độ phân giải
cap.set(4, 120)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)


main_window = tk.Tk()
main_window.title("PCBA Classifier")
main_window.geometry("640x480")

# Initialize the serial connection
arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)


#main frame setup
main_frame=tk.Frame(main_window)
main_frame.pack(fill="both",expand=True)
#grid main frame
main_frame.grid_columnconfigure((0,1,2,3,4,5), weight=1)
main_frame.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
text_style=font.Font(family="Arial",size=12,weight="normal")

def create_label_frame(partent, title, row, column, rowspan, columnspan):
    frame=tk.LabelFrame(partent,text=title,font=text_style,width=10)
    frame.grid(row=row,column=column,rowspan=rowspan,columnspan=columnspan,padx=1,pady=1,sticky="nsew")
    return frame

#create label frame
image_labelframe=create_label_frame(main_frame, "Image", 0, 0, 3, 3)
tray_status_labelframe=create_label_frame(main_frame, "Tray Status", 0, 3, 4, 4)
result_labelframe=create_label_frame(main_frame, "Result", 3, 0, 3, 3)
console_labelframe=create_label_frame(main_frame, "Console Log", 6, 0, 1, 6)
process_labelframe=create_label_frame(main_frame, "Process", 4, 3, 2, 1)
control_labelframe=create_label_frame(main_frame, "Control", 4, 4, 2, 2)

image_labelframe.grid_propagate(False)
tray_status_labelframe.grid_propagate(False)
result_labelframe.grid_propagate(False)
console_labelframe.grid_propagate(False)
process_labelframe.grid_propagate(False)
control_labelframe.grid_propagate(False)

#create imagelabel
image_labelframe.grid_columnconfigure((0,1), weight=1)
image_labelframe.grid_rowconfigure((0), weight=1)
frame_label = Label(image_labelframe)
frame_label.grid(row=0,column=1,sticky="ns")
preview_label = Label(image_labelframe)
preview_label.grid(row=0,column=0,sticky="ns")

detection_get_points = []
PCBAmodel = YOLO("models/PCBA.pt")
ParScrModel=YOLO("models/ParScrDet.pt")
frame_queue = Queue() #Queue to hold processed frame
current_frame = None
def update_preview():
    global current_frame
    ret, frame = cap.read()
    if ret:
        cv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv_img)
        img_tk = ImageTk.PhotoImage(image=img)

        preview_label.config(image = img_tk)
        preview_label.image = img_tk

        current_frame = frame
    main_window.after(10, update_preview)
update_preview()

output_directory = "captured_tray"
os.makedirs(output_directory, exist_ok = True)
def save_frame():
    if current_frame is not None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(output_directory, f"captured_{timestamp}.jpg")

        cv2.imwrite(file_path, current_frame)
        print(f"Frame saved as: {file_path}")

def capture_and_detect():
    save_frame()
    global current_frame
    global detection_get_points
    detection_get_points.clear()#empty before get new one
    if current_frame is not None:
        
        results = PCBAmodel(current_frame)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2-x1, y2-y1
                cvzone.cornerRect(current_frame, (x1, y1, w, h))
                detection_get_points.append([x1, y1, w, h])
        

        global detection_array
        detection_array = np.array(detection_get_points)

        # Convert processed frame for display in Tkinter
        img_pil = Image.fromarray(cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(image=img_pil)
        frame_label.config(image=img_tk)
        frame_label.image = img_tk  # Keep a reference


def update_frame():
    if not frame_queue.empty():
        img_tk = frame_queue.get()
        frame_label.config(image = img_tk)
        frame_label.image = img_tk
    main_window.after(5, update_frame)
    

def Par_Scr_detect():
    global current_frame
    time.sleep(5)
    if current_frame is not None:
        check_results = ParScrModel(current_frame)
        object_detected = False
        for r in check_results:
            if r.boxes:  # Check if there are boxes
                object_detected = True
                for box in r.boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    cvzone.cornerRect(current_frame, (x1, y1, w, h))
        # Convert processed frame for display in Tkinter
        sensor_img_pil = Image.fromarray(cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB))
        sensor_img_tk = ImageTk.PhotoImage(image=sensor_img_pil)
        frame_label.config(image=sensor_img_tk)
        frame_label.image = sensor_img_tk  # Keep a reference

        # Print result based on detection status
        if object_detected:
            print("NG")  # Objects detected
            send_command("NG")
            increment_NG(red_label,green_label,blue_label)
        else:
            print("Pass")  # No objects detected
            send_command("Pass")
            increment_OK(green_label,red_label,blue_label)

#grid controlfarme
control_labelframe.grid_columnconfigure((0,1),weight=1)
control_labelframe.grid_rowconfigure((0,1),weight=1)

#define create button function
def create_button(text,bg,row,col, command, state=tk.NORMAL):
    button=tk.Button(control_labelframe,text=text,background=bg,font=text_style,command=command, state = state)
    button.grid(row=row,column=col,padx=5,pady=5,sticky="nsew")
    return button

home_pressed = False

#create control button
Home_button=create_button("Home","lightgray",0,0, lambda: press_home())
Emergency_button=create_button("Emergency","red",0,1,lambda: None)
# Emergency_button=create_button("Emergency","red",0,1,lambda: capture_and_detect())
Start_button=create_button("Start","lightgray",1,0, lambda: start_process(), state = tk.DISABLED)
Stop_button=create_button("Stop","lightgray",1,1,lambda: send_command("RES"), state = tk.DISABLED)

def start_process():
    for i in range(1,5):
        change_led_color(i, "white")
    send_command("ITCP")

def press_home():
    global home_pressed
    home_pressed = True
    send_command("H")
    Start_button.config(state=tk.NORMAL)
    Stop_button.config(state=tk.NORMAL)

# Dictionary để lưu trữ các LED
leds = {}

def change_led_color(step_number, color="green"):
    led = leds.get(step_number)
    if led:
        led.config(bg=color)

# Hàm để tạo LED và Label cho mỗi bước quá trình
def create_process_step(frame, text, row, columnspan=2):
    LED = tk.Label(frame, bg="white", borderwidth=2, relief="raised")
    LED.grid(row=row, column=0, sticky="nsew", padx=5, pady=5)
    leds[row] = LED  # Lưu trữ LED vào dictionary

    step_label = tk.Label(frame, text=text, font=text_style)
    step_label.grid(row=row, column=1, columnspan=columnspan, sticky="W", padx=5, pady=5)

# Tạo các bước quá trình và nút tương ứng
steps = ["Home", "Tray Check", "Sensor Check", "Classify", "Finish"]
for i, step in enumerate(steps):
    process_labelframe.grid_rowconfigure(i, weight=1)
    process_labelframe.grid_columnconfigure((0, 1, 2), weight=1)
    create_process_step(process_labelframe, step, i)

#config number font
num_font=font.Font(family="Arial",size=50,weight="bold")

#define create label function
def create_result_label( text,font, fg, bg, row, column, rowspan):
    label=tk.Label(result_labelframe,text=text, font=font, fg=fg, bg=bg)
    label.grid(row=row, rowspan=rowspan, column=column, sticky="nsew")
    return label

#define number increment
def increment_OK(ok_label, ng_label, total_label):
    current_ok_value=int(ok_label["text"])
    ok_label.config(text=str(current_ok_value+1))
    #upgrade total
    update_total(ok_label, ng_label, total_label)

def increment_NG(ng_label, ok_label, total_label):
    # Tăng số lượng NG
    current_ng_value = int(ng_label["text"])
    ng_label.config(text=str(current_ng_value + 1))
    
    # Cập nhật tổng số
    update_total(ok_label, ng_label, total_label)

def update_total(ok_label, ng_label, total_label):
    # Tính toán tổng mới và cập nhật label Total
    total_value = int(ok_label["text"]) + int(ng_label["text"])
    total_label.config(text=str(total_value))

#grid result label
result_labelframe.columnconfigure((0, 1, 2), weight=1)
result_labelframe.rowconfigure((0, 1, 2), weight=1)

#create label for result frame
OK_label=create_result_label("OK Qty", text_style, "black", "lightgray" , 0, 0, 1)
NG_label=create_result_label("NG Qty", text_style, "black", "lightgray" , 0, 1, 1)
Total_label=create_result_label("Total Qty", text_style, "black", "lightgray" , 0, 2, 1)
green_label=create_result_label("0", num_font, "white","green", 1, 0, 2)
red_label=create_result_label("0", num_font, "white","red", 1, 1, 2)
blue_label=create_result_label("0", num_font, "white","blue", 1, 2, 2)

#### FOR TRAY STATUS 
virtual_points = np.array([
    [38, 24],
    [77, 24],
    [116, 24],
    [40, 64],
    [78, 64],
    [115, 64],
    [40, 101],
    [80, 100],
    [117, 98]
])


rows = 3 
columns = 3 
tray_names = ["Input", "OK", "NG"]
frames = {}
cell_labels = {}

#grid traystatus labelframe
tray_status_labelframe.grid_columnconfigure((0, 1, 2), weight=1)
tray_status_labelframe.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

wait_for_check = []
ok_place = []
ng_place = []

def threaded_function(func):
    def wrapper():
        thread = threading.Thread(target = func)
        thread.start()
    return wrapper 
def check_status(real_points, name):
    global wait_for_check, ok_place, ng_place

    # Làm trống danh sách trước khi thêm dữ liệu mới
    if name == "Input":
        wait_for_check.clear()
        
    elif name == "OK":
        ok_place.clear()
        
    elif name == "NG":
        ng_place.clear()
        
    point_status = []

    for index, (vp_x, vp_y) in enumerate(virtual_points):
        status = False
        for (x1, y1, w, h) in detection_array:
            if x1 <= vp_x <x1 + w and y1 <= vp_y < y1 + h:
                status = True
                break
        
        if status:
            if name == "Input":
                wait_for_check.append(real_points[index]) #save into the wait for check
                # print(wait_for_check)
                
        else:
            if name == "OK":
                ok_place.append(real_points[index]) #save the real point
                # print(ok_place)
                
            elif name == "NG":
                ng_place.append(real_points[index]) #save the real point
                # print(ng_place)

        point_status.append(status)
    for i, status in enumerate(point_status):
        cell_labels[name][i].config(bg='yellow' if status else 'lightgray')

    detected_count = sum(point_status)
    thread_add_log_message(f"{name} Tray - Number of detected PCBA: {detected_count}")
    
    #send points after checking
    if name == "Input":
        send_coordinates(wait_for_check, "waitForCheck")
        send_command("OTCP")
    elif name == "OK":
        send_coordinates(ok_place, "OKPlace")
        send_command("NTCP")
    elif name == "NG":
        send_coordinates(ng_place, "NGPlace")
        thread_add_log_message("Complete Tray Check")
        change_led_color(1)


def send_coordinates(points, label):
    for point in points:
        message = f"{label},{point[0]},{point[1]}\n"
        arduino.write(message.encode())
        time.sleep(0.6)
    send_command("CapOK")
    if label == "NGPlace":
        send_command("Check Sensor")


    
#create label and frame
for index, name in enumerate(tray_names):
    # create label
    label = tk.Label(tray_status_labelframe, text=name)
    label.grid(row=0, column=index, padx=10, pady=5)

    #create table_frame
    frame = tk.Frame(tray_status_labelframe, borderwidth=1, relief='solid')
    frame.grid(row=1, column=index, rowspan=4, padx=5, pady=5, sticky='nsew')
    frames[name]=frame
    cell_labels[name]=[]

    

    # Tạo lưới các ô trong mỗi bảng
    for row in range(rows):
        for col in range(columns):
            cell_label = tk.Label(frame, bg='lightgray',text=str(row*columns+col+1), width=4, height=2, borderwidth=1, relief='solid')
            cell_label.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)
            cell_labels[name].append(cell_label)

    # Đặt trọng số cho grid để các ô co giãn đều
    for row in range(rows):
        frame.grid_rowconfigure(row, weight=1)
    for col in range(columns):
        frame.grid_columnconfigure(col, weight=1)

#check Input tray status
def check_input():
    real_points_input = np.array([
        [-157, -285],
        [-157, -256],
        [-157, -227],
        [-128, -285],
        [-128, -256],
        [-128, -227],
        [-99, -285],
        [-99, -256],
        [-99, -227]
    ])
    check_status(real_points_input, "Input")
#check OK tray status
def check_OK():
    real_points_ok = np.array([
        [-138, -278],
        [-138, -249],
        [-138, -220],
        [-109, -278],
        [-109, -249],
        [-109, -220],
        [-80, -278],
        [-80, -249],
        [-80, -220]
    ])
    check_status(real_points_ok, "OK")
#check NG tray status
def check_NG():
    real_points_ng = np.array([
        [-187, -161],
        [-187, -132],
        [-187, -103],
        [-158, -161],
        [-158, -132],
        [-158, -103],
        [-129, -161],
        [-129, -132],
        [-129, -103] 
    ])
    check_status(real_points_ng, "NG")

#create console text inside console labelframe
console_log=tk.Text(console_labelframe,height=0.5,fg="white", background="#3A3939")
scrollbar = tk.Scrollbar(console_log, command=console_log.yview)
console_log.configure(yscrollcommand=scrollbar.set)
console_log.pack(fill="both",expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def thread_add_log_message(message):
    # Lên lịch hàm add_log_message để chạy trên luồng chính
    main_window.after(0, lambda: add_log_message(message))

#function add log 
def add_log_message(message):
    console_log.insert(tk.END, message + '\n')
    console_log.see(tk.END)  # Cuộn đến dòng mới nhất


# Function to send command to Arduino
def send_command(command):
    command_code = f"{command}\n"
    arduino.write(command_code.encode())
    time.sleep(0.5)

# Function to continuously read from serial
def read_from_serial(console_log):
    while True:
        if arduino.in_waiting > 0:
            received = arduino.readline().decode('utf-8').rstrip()
            console_log.insert(tk.END, received + "\n")
            console_log.see(tk.END)

            if received == "Detect Input Tray":
                cap.set(cv2.CAP_PROP_FOCUS,60)
                time.sleep(1)
                capture_and_detect()
                threaded_function(check_input)()
                # time.sleep(1)
                # send_command("OTCP")
            elif received == "Detect OK Tray":
                capture_and_detect()
                threaded_function(check_OK)()
                # time.sleep(1)
                # send_command("NTCP")
            elif received == "Detect NG Tray":
                capture_and_detect()
                threaded_function(check_NG)()
                send_command("LampClose")
                
                cap.set(cv2.CAP_PROP_FOCUS,255)
            elif received == "ParScrCheck":
                Par_Scr_detect()
            elif received == "Returned to origin.":
                change_led_color(0)    
            elif received == "Sensor check completed":
                change_led_color(2)
            elif received == "Classification completed":
                change_led_color(3)     
                change_led_color(4)
            elif received == "Classification completed":
                change_led_color(3)     
                change_led_color(4)    




# Start the thread to read from serial
thread = threading.Thread(target=read_from_serial, args=(console_log,))
thread.daemon = True
thread.start()

main_window.mainloop()
arduino.close()
cap.release()
cv2.destroyAllWindows()




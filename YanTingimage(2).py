import tkinter as tk
from tkinter import font
from tkinter import Button, Label, LabelFrame
import time
from ultralytics import YOLO
import cv2
from PIL import Image, ImageTk

# ----------------------------
# 1. 主視窗設定
# ----------------------------
window = tk.Tk()
window.title("classifier")
window.geometry("750x480")

# ----------------------------
# 2. 載入 YOLOv8 權重 (papertube.pt)
#    請確認 papertube.pt 與此程式放在同一層資料夾
# ----------------------------
model = YOLO("papertube.pt")  # 只載入這一個模型
time.sleep(2)  # 等待模型初始化

# ----------------------------
# 3. 開啟攝影機
# ----------------------------
cap = cv2.VideoCapture(0)
# （可視需要設定解析度，例如 640x480）
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ----------------------------
# 4. 建立主框架與左右子框架
# ----------------------------
main_frame = tk.Frame(window, bg="#83A6CE")
main_frame.pack(fill="both", expand=True)

left_frame = tk.Frame(main_frame)
left_frame.grid(padx=(10, 0), pady=(5, 10), row=0, column=0, sticky="nsew")

right_frame = tk.Frame(main_frame)
right_frame.grid(padx=(0, 10), pady=(5, 10), row=0, column=1, sticky="nsew")

# ----------------------------
# 5. 建立 LabelFrame：Process、Control、Image、Result、Status、Console Log
# ----------------------------
# Process 區（如果未來需要放流程燈之類的，可自行改）
process_label_frame = LabelFrame(left_frame, text="Process", background="#83A6CE")
process_label_frame.grid(row=1, column=1, sticky="nsew")

# Control 區（如果未來要放按鈕，可自行改）
control_label_frame = LabelFrame(left_frame, text="Control", background="#83A6CE")
control_label_frame.grid(row=1, column=0, sticky="nsew")

# Image 區（顯示 YOLO 推論後結果）
image_label_frame = LabelFrame(left_frame, text="Image", background="#83A6CE")
image_label_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
image_label_frame.grid_propagate(False)

# 影像顯示的 Label
image_label = Label(image_label_frame, width=480, height=240, bg="#83A6CE", borderwidth=0, highlightthickness=0)
image_label.place(x=0, y=0)

# Result 區
result_label_frame = LabelFrame(right_frame, text="Result", background="#83A6CE")
result_label_frame.pack(fill="both", expand=True)

# 在 Result 區裡放一個專門顯示 OK/NG 狀態的 Label
status_text = font.Font(family="Arial", size=36, weight="bold")
status_label = Label(result_label_frame, text="--", font=status_text, width=10, bg="#BBBBBB", fg="white")
status_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# Status 區（如果你想另外放圖示圓燈之類的 Region，可以自行修改）
status_label_frame = LabelFrame(result_label_frame, text="Status Light", background="#83A6CE")
status_label_frame.grid(row=1, rowspan=2, column=0, padx=10, pady=10, sticky="nsew")

# Control 下面額外放一個 Console Log
console_frame = LabelFrame(result_label_frame, text="Console Log", background="#83A6CE")
console_frame.grid(row=3, rowspan=2, column=0, padx=10, pady=10, sticky="nsew")
console_log = tk.Text(console_frame, wrap=tk.WORD, state="normal", bg="white", height=3)
console_log.pack(fill="both", expand=True, padx=5, pady=5)

# ----------------------------
# 6. 設定各區段的 Grid 伸縮行列比例
# ----------------------------
main_frame.grid_columnconfigure((0, 1), weight=1)
main_frame.grid_rowconfigure(0, weight=1)

left_frame.grid_rowconfigure((0, 1), weight=1)
left_frame.grid_columnconfigure((0, 1), weight=1)

right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

# 如果未來 Process/Control 有內容，可同樣設定
control_label_frame.grid_columnconfigure(0, weight=1)
control_label_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

process_label_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
process_label_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

# ----------------------------
# 7. 如果需要，Control 區可塞一些按鈕（此範例先留空）
# ----------------------------
# button_text_style = font.Font(family="Arial", size=12, weight="normal")
# start_button = Button(control_label_frame, text="Start", command=None, font=button_text_style)
# start_button.grid(padx=10, pady=10, row=0, column=0, sticky="nsew")
# ...

# ----------------------------
# 8. Process 區示範（若要放流程步驟提示，可自行更改）
# ----------------------------
# text_style = font.Font(family="Arial", size=12, weight="normal")
# steps = ["Moving", "Detection", "Classification", "Finish"]
# for i, step in enumerate(steps):
#     light = Label(process_label_frame, bg="white")
#     light.grid(row=i, column=0, padx=25, pady=25, sticky="nsew")
#     step_label = Label(process_label_frame, text=step, font=text_style, anchor="w")
#     step_label.grid(row=i, column=1, columnspan=5, padx=15, pady=15, sticky="nsew")

# ----------------------------
# 9. 定義 update_frame(): 每 100ms 擷取一幀 → 執行 YOLOv8 推論 → 疊框 → 判斷 OK/NG → 顯示
# ----------------------------
def update_frame():
    ret, frame = cap.read()
    if not ret:
        window.after(100, update_frame)
        return

    # 9.1 將 BGR 轉為 RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 9.2 呼叫 YOLOv8 模型做推論
    results = model(rgb_frame)            # 傳入 RGB 影像
    annotated = results[0].plot()         # .plot() 會把盒子、label、conf 疊到影像上

    # 9.3 判斷 NG 邏輯：如果 boxes 非空，就代表有至少一個物件 → NG；否則 OK
    if len(results[0].boxes) > 0:
        # 有偵測到東西 → NG
        status_label.config(text="NG", bg="#E44C5E")
        console_log.insert(tk.END, "Detect: NG\n")
    else:
        # 沒偵測到 → OK
        status_label.config(text="OK", bg="#4CE461")
        console_log.insert(tk.END, "Detect: OK\n")

    # 9.4 把 annotated (RGB numpy) 轉成 PIL Image，再轉成 PhotoImage
    img_pil = Image.fromarray(annotated)
    img_pil = img_pil.resize((480, 240))  # 調整成 Label 規定大小
    img_tk  = ImageTk.PhotoImage(image=img_pil)

    # 9.5 更新到 image_label
    image_label.configure(image=img_tk)
    image_label.imgtk = img_tk

    # 9.6 每隔 100ms 再呼叫自己，形成連續更新
    window.after(100, update_frame)

# 啟動第一個影格更新
update_frame()

# ----------------------------
# 10. 啟動 Tkinter 主迴圈並釋放資源
# ----------------------------
window.mainloop()
cap.release()
cv2.destroyAllWindows()

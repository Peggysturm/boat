import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk

def calculate_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def find_color_objects(frame, lower_color, upper_color, blur_ksize, min_distance, min_area):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blurred_frame = cv2.GaussianBlur(hsv_frame, (blur_ksize, blur_ksize), 0)
    mask = cv2.inRange(blurred_frame, lower_color, upper_color)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    objects_info = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                objects_info.append({'contour': contour, 'center': (cX, cY), 'area': area})

    filtered_objects = []
    for i, obj1 in enumerate(objects_info):
        too_close = False
        for j, obj2 in enumerate(objects_info):
            if i != j:
                distance = calculate_distance(obj1['center'], obj2['center'])
                if distance < min_distance:
                    if obj1['area'] < obj2['area']:
                        too_close = True
                        break
        if not too_close:
            filtered_objects.append(obj1)

    return filtered_objects

def update_trackbar_value(value, label, var):
    """Функция для обновления значений трекбаров"""
    var.set(value)
    label.config(text=f"{label.cget('text').split(':')[0]}: {value}")

def nothing(x):
    pass


root = tk.Tk()
root.title("Settings")


main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


trackbar_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=trackbar_frame, anchor="nw")


lower_h_yellow = tk.IntVar(value=20)
lower_s_yellow = tk.IntVar(value=100)
lower_v_yellow = tk.IntVar(value=100)
upper_h_yellow = tk.IntVar(value=30)
upper_s_yellow = tk.IntVar(value=255)
upper_v_yellow = tk.IntVar(value=255)

lower_h_green = tk.IntVar(value=35)
lower_s_green = tk.IntVar(value=100)
lower_v_green = tk.IntVar(value=100)
upper_h_green = tk.IntVar(value=85)
upper_s_green = tk.IntVar(value=255)
upper_v_green = tk.IntVar(value=255)

lower_h_blue = tk.IntVar(value=90)
lower_s_blue = tk.IntVar(value=100)
lower_v_blue = tk.IntVar(value=100)
upper_h_blue = tk.IntVar(value=130)
upper_s_blue = tk.IntVar(value=255)
upper_v_blue = tk.IntVar(value=255)

blur_ksize = tk.IntVar(value=5)
min_distance = tk.IntVar(value=50)
min_area = tk.IntVar(value=100)

enable_yellow = tk.BooleanVar(value=True)
enable_green = tk.BooleanVar(value=True)
enable_blue = tk.BooleanVar(value=True)

sliders = [
    ("Lower H - Yellow", lower_h_yellow),
    ("Lower S - Yellow", lower_s_yellow),
    ("Lower V - Yellow", lower_v_yellow),
    ("Upper H - Yellow", upper_h_yellow),
    ("Upper S - Yellow", upper_s_yellow),
    ("Upper V - Yellow", upper_v_yellow),
    ("Lower H - Green", lower_h_green),
    ("Lower S - Green", lower_s_green),
    ("Lower V - Green", lower_v_green),
    ("Upper H - Green", upper_h_green),
    ("Upper S - Green", upper_s_green),
    ("Upper V - Green", upper_v_green),
    ("Lower H - Blue", lower_h_blue),
    ("Lower S - Blue", lower_s_blue),
    ("Lower V - Blue", lower_v_blue),
    ("Upper H - Blue", upper_h_blue),
    ("Upper S - Blue", upper_s_blue),
    ("Upper V - Blue", upper_v_blue),
    ("Blur ksize", blur_ksize),
    ("Min Distance", min_distance),
    ("Min Area", min_area),
]
slider_limits = {
    "Lower H - Yellow": (0, 179),
    "Lower S - Yellow": (0, 255),
    "Lower V - Yellow": (0, 255),
    "Upper H - Yellow": (0, 179),
    "Upper S - Yellow": (0, 255),
    "Upper V - Yellow": (0, 255),
    "Lower H - Green": (0, 179),
    "Lower S - Green": (0, 255),
    "Lower V - Green": (0, 255),
    "Upper H - Green": (0, 179),
    "Upper S - Green": (0, 255),
    "Upper V - Green": (0, 255),
    "Lower H - Blue": (0, 179),
    "Lower S - Blue": (0, 255),
    "Lower V - Blue": (0, 255),
    "Upper H - Blue": (0, 179),
    "Upper S - Blue": (0, 255),
    "Upper V - Blue": (0, 255),
    "Blur ksize": (1, 25),
    "Min Distance": (0, 50000),
    "Min Area": (0, 1000000)
}

for label_text, var in sliders:
    frame = ttk.Frame(trackbar_frame)
    frame.pack(pady=5, padx=10, fill=tk.X)

    slider_min, slider_max = slider_limits[label_text]
    
    label = ttk.Label(frame, text=f"{label_text}: {var.get()}")
    label.pack(side=tk.LEFT)

    slider = ttk.Scale(frame, from_=slider_min, to=slider_max, variable=var, orient=tk.HORIZONTAL, length=200)
    slider.pack(side=tk.RIGHT)
    
    slider.config(command=lambda value, lbl=label, vr=var: update_trackbar_value(int(float(value)), lbl, vr))

checkbutton_frame = ttk.Frame(trackbar_frame)
checkbutton_frame.pack(pady=10, padx=10, fill=tk.X)

yellow_check = ttk.Checkbutton(checkbutton_frame, text="Enable Yellow", variable=enable_yellow)
yellow_check.pack(anchor=tk.W)

green_check = ttk.Checkbutton(checkbutton_frame, text="Enable Green", variable=enable_green)
green_check.pack(anchor=tk.W)

blue_check = ttk.Checkbutton(checkbutton_frame, text="Enable Blue", variable=enable_blue)
blue_check.pack(anchor=tk.W)

cap = cv2.VideoCapture(0)

def video_loop():
    ret, frame = cap.read()
    if not ret:
        root.quit()

    blur_size = blur_ksize.get()
    if blur_size % 2 == 0:
        blur_size += 1

    min_dist = min_distance.get()
    min_ar = min_area.get()

    if enable_yellow.get():
        lower_yellow = np.array([lower_h_yellow.get(), lower_s_yellow.get(), lower_v_yellow.get()])
        upper_yellow = np.array([upper_h_yellow.get(), upper_s_yellow.get(), upper_v_yellow.get()])
        yellow_objects = find_color_objects(frame, lower_yellow, upper_yellow, blur_size, min_dist, min_ar)
        for obj in yellow_objects:
            cv2.drawContours(frame, [obj['contour']], -1, (0, 255, 255), 2)
            cv2.circle(frame, obj['center'], 5, (0, 255, 255), -1)
            cv2.putText(frame, f'Area: {int(obj["area"])}', (obj['center'][0] + 10, obj['center'][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    if enable_green.get():
        lower_green = np.array([lower_h_green.get(), lower_s_green.get(), lower_v_green.get()])
        upper_green = np.array([upper_h_green.get(), upper_s_green.get(), upper_v_green.get()])
        green_objects = find_color_objects(frame, lower_green, upper_green, blur_size, min_dist, min_ar)
        for obj in green_objects:
            cv2.drawContours(frame, [obj['contour']], -1, (0, 255, 0), 2)
            cv2.circle(frame, obj['center'], 5, (0, 255, 0), -1)
            cv2.putText(frame, f'Area: {int(obj["area"])}', (obj['center'][0] + 10, obj['center'][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    if enable_blue.get():
        lower_blue = np.array([lower_h_blue.get(), lower_s_blue.get(), lower_v_blue.get()])
        upper_blue = np.array([upper_h_blue.get(), upper_s_blue.get(), upper_v_blue.get()])
        blue_objects = find_color_objects(frame, lower_blue, upper_blue, blur_size, min_dist, min_ar)
        for obj in blue_objects:
            cv2.drawContours(frame, [obj['contour']], -1, (255, 0, 0), 2)
            cv2.circle(frame, obj['center'], 5, (255, 0, 0), -1)
            cv2.putText(frame, f'Area: {int(obj["area"])}', (obj['center'][0] + 10, obj['center'][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    cv2.imshow("Frame", frame)

    root.after(10, video_loop)

root.after(10, video_loop)
root.mainloop()

cap.release()
cv2.destroyAllWindows()
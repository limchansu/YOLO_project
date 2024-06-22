import numpy as np
from datetime import datetime
from ultralytics import YOLO
import cv2
import socket
import json
import tkinter as tk
from tkinter import messagebox

def send_data_to_counter(data):
    host = 'localhost'
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(data.encode('utf-8'))

def ask_for_payment(detected_products, timestamp):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    answer = messagebox.askyesno("Payment Confirmation", f"Products: {', '.join(detected_products)}\nDo you want to proceed with the payment?")
    if answer:
        data = json.dumps({"products": detected_products, "timestamp": timestamp})
        send_data_to_counter(data)
    root.destroy()

def use_result(results, frame, detected_products_set):
    new_detected_products = []  

    if results and results[0]:
        bboxes = np.array(results[0].boxes.xyxy.cpu(), dtype="int")
        classes = np.array(results[0].boxes.cls.cpu(), dtype="int")
        names = results[0].names

        pred_box = zip(classes, bboxes)

        for cls, bbox in pred_box:
            (x, y, x2, y2) = bbox
            if names[cls] not in detected_products_set:  
                detected_products_set.add(names[cls])
                new_detected_products.append(names[cls])

                cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, str(names[cls]), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    if new_detected_products:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ask_for_payment(new_detected_products, current_time)

    return frame

if __name__ == "__main__":
    custom_model_path = "C:/Temp/custom_training/object/runs/detect/train/weights/best.pt"
    model = YOLO(custom_model_path)

    video_path = "./calculator실험.mp4"
    cap = cv2.VideoCapture(video_path)

    detected_products_set = set()  
    payment_prompted = False  

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        new_frame = use_result(results, frame, detected_products_set)
        
        if detected_products_set and not payment_prompted:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ask_for_payment(list(detected_products_set), current_time)
            payment_prompted = True  

        cv2.imshow("Img", new_frame)

        key = cv2.waitKey(1)
        if key == 27:  
            break

    cap.release()
    cv2.destroyAllWindows()

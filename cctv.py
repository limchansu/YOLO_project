import numpy as np
from datetime import datetime, timedelta
from ultralytics import YOLO
import cv2
import socket
import json

def send_data_to_server(data):
    host = 'localhost'
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(data.encode('utf-8'))

def use_result(results, frame, person_detected, first_detected_time, last_detected_time, cctv_records):
    if results and results[0]:
        bboxes = np.array(results[0].boxes.xyxy.cpu(), dtype="int")
        classes = np.array(results[0].boxes.cls.cpu(), dtype="int")
        names = results[0].names

        pred_box = zip(classes, bboxes)
        detected_person = False

        for cls, bbox in pred_box:
            (x, y, x2, y2) = bbox

            if names[cls] == "person":
                cv2.rectangle(frame, (x, y), (x2, y2), (0,0,255), 2)
                cv2.putText(frame, names[cls], (x, y-5), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
                
                current_time = datetime.now()
                print("Person detected at:", current_time.strftime("%Y-%m-%d %H:%M:%S"))
                if not person_detected:
                    first_detected_time = current_time
                    person_detected = True
                last_detected_time = current_time
                detected_person = True
        
        if not detected_person and person_detected:
            # 사람이 마지막으로 탐지된 시간으로부터 일정 시간이 지난 후 데이터를 전송
            if (datetime.now() - last_detected_time).seconds > 5:  # 5초 후 데이터 전송
                cctv_records.append((first_detected_time, last_detected_time))  # CCTV 기록 추가
                data = json.dumps({
                    "start_time": first_detected_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "end_time": last_detected_time.strftime("%Y-%m-%d %H:%M:%S")
                })
                send_data_to_server(data)
                person_detected = False
                first_detected_time = None
                last_detected_time = None

    scale_percent = 100
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    frame_s = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow("Img", frame_s)
    
    return person_detected, first_detected_time, last_detected_time, cctv_records

if __name__ == "__main__":
    model = YOLO("yolov8n.pt")

    video_path = "./cctv실험.mp4"
    cap = cv2.VideoCapture(video_path)

    person_detected = False
    first_detected_time = None
    last_detected_time = None
    cctv_records = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        person_detected, first_detected_time, last_detected_time, cctv_records = use_result(
            results, frame, person_detected, first_detected_time, last_detected_time, cctv_records
        )
        
        # 키보드 입력 처리
        key = cv2.waitKey(1)
        if key == 27:  # ESC 키를 누르면 종료
            break

    cap.release()
    cv2.destroyAllWindows()

    # CCTV 기록 전송
    for start_time, end_time in cctv_records:
        data = json.dumps({
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S")
        })
        send_data_to_server(data)

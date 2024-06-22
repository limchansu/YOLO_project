from ultralytics import YOLO

# 데이터셋 경로와 모델 경로 설정
data_path = "C:/Temp/custom_training/object/YOLODataset/dataset.yaml"
model_path = "yolov8m.pt"

# YOLO 모델 초기화
model = YOLO(model_path)

# 모델 학습
model.train(data=data_path, epochs=5)

# 학습이 완료된 모델을 저장
model.save("C:/Temp/custom_training/object/YOLODataset/best.pt")
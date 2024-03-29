from ultralytics import YOLO

model = YOLO('weights/yolov8x.pt') 

# Train the model
results = model.train(data='dataset/dataset.yaml', epochs=100, imgsz=320, device='mps')
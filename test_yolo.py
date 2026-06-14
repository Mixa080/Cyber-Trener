import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8n-pose.pt')
frame = np.zeros((480, 640, 3), dtype=np.uint8)
results = model(frame)
try:
    ann = results[0].plot(img=frame)
    print("plot(img=) worked")
except Exception as e:
    print(f"Error: {e}")

from ultralytics import YOLO
import torch
import cv2
import os
import numpy as np


model = YOLO('yolo11n.pt')  # load a pretrained YOLO detection model
def detect_objects(image_path):
    """
    Detect objects in the given image using the YOLOv8 model.
    """
    # Load image
    print('____________________', os.listdir('uploads'))
    image_path = os.path.join('uploads', 'images', os.path.basename(image_path))
    print('______________________________', image_path)
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Perform detection
    results = model.predict(image_path, conf=0.25)

    # Parse the results to extract detected object names
    detected_objects = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)  # Class ID
            class_name = model.names[class_id]  # Map class ID to name
            detected_objects.append(class_name)

    return detected_objects
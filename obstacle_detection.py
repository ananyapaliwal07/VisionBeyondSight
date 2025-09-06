from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # load YOLO model once globally

def detect_objects_from_frame(frame):
    results = model(frame)
    detected = []
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            detected.append(label)  # include all objects

    if detected:
        return ", ".join(detected)  # return all objects as string
    return None

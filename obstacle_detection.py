import cv2
from ultralytics import YOLO
import pyttsx3
import threading
import queue
import time
from speech import speak
# Queue for speech messages
speech_queue = queue.Queue()

def detect_obstacles():
    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(0)

    last_alert = None
    last_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]

                if label in ["person", "chair"]:
                    now = time.time()
                    if last_alert != label or (now - last_time) > 3:
                        speak(f"{label} ahead")
                        last_alert = label
                        last_time = now

        cv2.imshow("Obstacle Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    speech_queue.put("EXIT")  # stop speech thread

if __name__ == "__main__":
    detect_obstacles()


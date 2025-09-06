import threading
import time
import json
import base64
import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template
from obstacle_detection import detect_objects_from_frame  # your YOLO detection function
from navigation import get_navigation_route
from speech import stop_speech
from messages import add_message, messages
import os




app = Flask(__name__, template_folder="templates", static_folder="static")

# ===== Routes =====

@app.route("/start_navigation", methods=["POST"])
def start_navigation():
    destination_name = request.json.get("destination")

    def nav_task():
        nav_thread = threading.Thread(target=get_navigation_route, args=(destination_name,))
        nav_thread.start()
        nav_thread.join()
        stop_speech()

    threading.Thread(target=nav_task).start()
    return jsonify({"status": "Navigation started"})

@app.route("/get_latest_messages", methods=["GET"])
def get_latest_messages():
    return jsonify(messages)

@app.route("/get_location", methods=["GET"])
def get_location():
    # Replace with actual GPS if available
    return jsonify({"lat": 28.6139, "lng": 77.2090})

@app.route("/detect", methods=['POST'])
def detect():
    data = request.get_json()
    img_data = data.get("image", "")
    if not img_data:
        return jsonify({"object": None})

    # Convert base64 image to cv2 frame
    img_str = img_data.split(",")[1]
    img_bytes = base64.b64decode(img_str)
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    detected_obj = detect_objects_from_frame(frame)  # returns string like "person" or None
    if detected_obj:
        add_message(f"Obstacle detected: {detected_obj}")
    return jsonify({"object": detected_obj})

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

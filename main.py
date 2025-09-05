import threading
from flask import Flask, request, jsonify, render_template
from navigation import get_navigation_route
from obstacle_detection import detect_obstacles
from speech import stop_speech
import json
import time
from messages import add_message, messages

app = Flask(__name__, template_folder="E:/ananya's/hackQuanta/templates", static_folder="E:/ananya's/hackQuanta/static")

# Store messages for frontend
messages = []

def add_message(msg):
    messages.append(msg)
    # optional: save to JSON
    with open("../frontend/static/messages.json", "w") as f:
        json.dump(messages, f)

@app.route("/start_navigation", methods=["POST"])
def start_navigation():
    destination_name = request.json.get("destination")

    def nav_task():
        nav_thread = threading.Thread(target=get_navigation_route, args=(destination_name,))
        nav_thread.start()

        # Example: simulate messages instead of pyttsx3
        example_msgs = [
            "Navigation started!",
            "Obstacle ahead on left!",
            "Turn right in 5 meters!",
            "Obstacle cleared",
            "You have reached your destination"
        ]
        for msg in example_msgs:
            add_message(msg)
            time.sleep(2)  # simulate real-time

        detect_obstacles()
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

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

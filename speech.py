import pyttsx3
import threading
import queue

speech_queue = queue.Queue()

def speech_worker():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    while True:
        text = speech_queue.get()
        if text == "EXIT":
            break
        engine.say(text)
        engine.runAndWait()

    engine.stop()

speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()

def speak(text):
    speech_queue.put(text)

def stop_speech():
    speech_queue.put("EXIT")

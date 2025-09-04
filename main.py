import threading
from navigation import get_navigation_route
from obstacle_detection import detect_obstacles
from speech import stop_speech
import speech_recognition as sr

def get_voice_destination():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say your destination...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand. Try again.")
            return None
        except sr.RequestError:
            print("API unavailable.")
            return None

def main():
    destination_name = None
    while not destination_name:
        destination_name = get_voice_destination()

    # Start navigation in a separate thread
    nav_thread = threading.Thread(target=get_navigation_route, args=(destination_name,))
    nav_thread.start()

    # Start obstacle detection (runs in main thread)
    detect_obstacles()

    # Cleanup speech engine if needed
    stop_speech()

if __name__ == "__main__":
    main()

import googlemaps
from speech import speech_queue
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))


def get_navigation_route(destination, start_location="Maharaja Surajmal Institute of Technology, Delhi"):
    """Fetch walking navigation route and speak it step by step"""
    try:
        directions = gmaps.directions(start_location, destination, mode="walking", departure_time=datetime.now())

        if not directions:
            speech_queue.put("No route found.")
            return

        steps = directions[0]['legs'][0]['steps']
        for step in steps:
            # clean HTML instructions
            instruction = step['html_instructions']
            clean_instruction = (
                instruction.replace("<b>", "")
                .replace("</b>", "")
                .replace('<div style="font-size:0.9em">', " ")
                .replace("</div>", "")
            )
            print(clean_instruction)
            speech_queue.put(clean_instruction)  # ye bolne ke liye speech thread me jayega
            time.sleep(10)  # har step ke beech thoda gap
    except Exception as e:
        speech_queue.put(f"Navigation error: {e}")

import requests
from speech import speak  # your speech.py speak() function

# Start location: MSIT Janakpuri (Longitude, Latitude)
START_COORDS = (77.1025, 28.7041)

# OSRM endpoint for walking directions
OSRM_URL = "http://router.project-osrm.org/route/v1/foot/{start_lon},{start_lat};{end_lon},{end_lat}?overview=false&steps=true"

# Temporary mapping of spoken destination names to coordinates
DESTINATIONS = {
    "karkardooma": (77.2931, 28.6773),
    "connaught place": (77.2167, 28.6329),
    "ashok vihar": (77.1350, 28.7000)
}

def get_navigation_route(destination_name):
    """
    Takes a spoken destination name (text), converts it to coordinates,
    fetches step-by-step walking instructions from OSRM, and speaks them.
    """
    # Convert name to coordinates
    destination_coords = DESTINATIONS.get(destination_name.lower())
    if not destination_coords:
        speak("Destination not recognized. Please try again.")
        return

    # Prepare OSRM API URL
    url = OSRM_URL.format(
        start_lon=START_COORDS[0],
        start_lat=START_COORDS[1],
        end_lon=destination_coords[0],
        end_lat=destination_coords[1]
    )

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print("Error fetching route:", e)
        speak("Could not fetch route. Please try again.")
        return

    # Check if route exists
    if 'routes' not in data or len(data['routes']) == 0:
        speak("No route found.")
        return

    # Speak each step
    steps = data['routes'][0]['legs'][0]['steps']
    for step in steps:
        instruction = step.get('maneuver', {}).get('instruction', step.get('name', 'Continue'))

        print(instruction)
        speak(instruction)

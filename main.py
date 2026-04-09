from src.weather import get_weather, parse_weather
from dotenv import load_dotenv
import os

load_dotenv()

# TODO: centralise default location
location = os.getenv("LOCATION_NAME", "Melbourne")

try:
    data = get_weather(location)
    print(parse_weather(data))
except ValueError as e:
    print(f"Config error: {e}")
except RuntimeError as e:
    print(f"Error: {e}")
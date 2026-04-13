from dotenv import load_dotenv
import os
import httpx
from pydantic import BaseModel

class CurrentWeather(BaseModel):
    temperature_2m: float
    wind_speed_10m: float
    weather_code: int

class WeatherResponse(BaseModel):
    current: CurrentWeather

load_dotenv()

LOCATION_NAME = os.getenv("LOCATION_NAME","Melbourne")

# Melbourne coordinates — hardcoded for now, we'll make this dynamic later
COORDINATES = {
    "Melbourne": {
        "latitude":-37.8136,
        "longitude":144.9631
    }
}

def get_weather(location: str) -> WeatherResponse:
    coords = COORDINATES.get(location)
    if not coords:
        raise ValueError(f"Unknown location: {location}")
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "timezone": "Australia/Melbourne"
    }

    try:
        response = httpx.get(url, params = params, timeout = 10.0)
        response.raise_for_status()
        return WeatherResponse(**response.json())
    except httpx.TimeoutException:
        raise RuntimeError("Weather API timed out — check your connection")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"Weather API returned an error: {e.response.status_code}")
    except httpx.RequestError as e:
        raise RuntimeError(f"Could not reach Weather API: {e}")

def parse_weather(data: WeatherResponse) -> str:
    current = data.current
    temp = current.temperature_2m
    wind = current.wind_speed_10m
    return f"Temperature: {temp}°C | Wind: {wind} km/h"
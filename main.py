from src.weather import get_weather, parse_weather
from dotenv import load_dotenv
import os
import asyncio
import httpx


load_dotenv()

# TODO: centralise default location
location = os.getenv("LOCATION_NAME", "Melbourne")

async def main():
    try:
        async with httpx.AsyncClient() as client:
            data = await get_weather(client, location)
            print(parse_weather(data))
    except ValueError as e:
        print(f"Config error: {e}")
    except RuntimeError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
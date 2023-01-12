import os

from dotenv import load_dotenv

load_dotenv()

open_weather_token = os.getenv('weather_token')

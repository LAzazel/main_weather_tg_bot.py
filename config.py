import os

from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_TOKEN = os.getenv('OPEN_WEATHER_TOKEN')
TOKEN = os.getenv('TOKEN')

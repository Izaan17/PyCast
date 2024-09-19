from dotenv import load_dotenv
import os

load_dotenv('secret.env')
API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
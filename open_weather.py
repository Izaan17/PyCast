import requests
from typing import Tuple, Union, Optional


class OpenWeatherAPI:
    """
    A class to interact with the OpenWeather API and fetch weather data for a given city.
    """
    def __init__(self, api_key: str) -> None:
        """
        Initializes the OpenWeatherAPI instance with the given API key.

        :param api_key: The API key for accessing the OpenWeather API.
        """
        self.api_key = api_key

    def fetch_weather_data(self, city: str) -> Optional[Tuple[bool, Union[dict, str]]]:
        """
        Fetches weather data for a given city from the OpenWeather API.

        :param city: The name of the city for which to fetch weather data.
        :return: A tuple (status, data) where status is a boolean indicating if the request was successful,
                 and data is either a dictionary containing the weather data (if successful)
                 or a string with an error message (if failed).
                 Returns None in case of an exception.
        """
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            # Clean up the response data to simplify it
            if data["cod"] == 200:
                return True, {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": round(data["main"]["temp"], 1),
                    "feels_like": round(data["main"]["feels_like"], 1),
                    "temp_min": round(data["main"]["temp_min"], 1),
                    "temp_max": round(data["main"]["temp_max"], 1),
                    "condition": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "wind_deg": data["wind"]["deg"],
                    "cloudiness": data["clouds"]["all"],
                    "visibility": data["visibility"],
                    "sunrise": data["sys"]["sunrise"],
                    "sunset": data["sys"]["sunset"],
                    "timezone": data["timezone"]
                }
            else:
                return False, data['message']
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False, str(e)
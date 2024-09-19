import customtkinter
import constants
from open_weather import OpenWeatherAPI


class PyCast(customtkinter.CTk):
    """
    PyCast is a simple weather application that fetches and displays weather information for a given location using
    the OpenWeather API. It now supports switching between metric and imperial units.
    """
    def __init__(self, **kwargs) -> None:
        """
        Initializes the PyCast weather application.

        :param kwargs: Additional arguments passed to the CTk (customtkinter) parent class.
        """
        super().__init__(**kwargs)

        # OpenWeather API Handler
        self.weather_fetcher = OpenWeatherAPI(constants.API_KEY)

        # Set default unit to metric
        self.is_metric = True

        self.title("PyCast Weather App")
        self.geometry("500x650")  # Increased height to accommodate the new button
        self.configure(fg_color="#2C3E50")  # Dark blue-gray background

        # Create a main frame
        self.main_frame = customtkinter.CTkFrame(self, fg_color="#34495E", corner_radius=20)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # App title
        self.title_label = customtkinter.CTkLabel(self.main_frame, text="PyCast Weather",
                                                  font=("Helvetica", 24, "bold"), text_color="#ECF0F1")
        self.title_label.pack(pady=(20, 10))

        # Location input frame
        self.input_frame = customtkinter.CTkFrame(self.main_frame, fg_color="#2C3E50", corner_radius=10)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        # Location input entry
        self.location_entry = customtkinter.CTkEntry(self.input_frame, placeholder_text="Enter city name",
                                                     width=300, height=40, font=("Helvetica", 14))
        self.location_entry.pack(side="left", padx=(10, 5), pady=10)

        # Search button
        self.search_button = customtkinter.CTkButton(self.input_frame, text="Search", command=self.get_weather,
                                                     width=100, height=40, font=("Helvetica", 14, "bold"),
                                                     fg_color="#3498DB", hover_color="#2980B9")
        self.search_button.pack(side="right", padx=(5, 10), pady=10)

        # Unit switch button
        self.unit_switch = customtkinter.CTkButton(self.main_frame, text="Switch to °F",
                                                   command=self.toggle_units, width=120, height=30,
                                                   font=("Helvetica", 12), fg_color="#E74C3C", hover_color="#C0392B")
        self.unit_switch.pack(pady=(0, 10))

        # Weather information display frame
        self.weather_frame = customtkinter.CTkFrame(self.main_frame, fg_color="#34495E", corner_radius=15)
        self.weather_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # City name label
        self.city_label = customtkinter.CTkLabel(self.weather_frame, text="",
                                                 font=("Helvetica", 22, "bold"), text_color="#ECF0F1")
        self.city_label.pack(pady=(20, 10))

        # Temperature label
        self.temp_label = customtkinter.CTkLabel(self.weather_frame, text="",
                                                 font=("Helvetica", 48, "bold"), text_color="#F39C12")
        self.temp_label.pack(pady=10)

        # Weather condition label
        self.condition_label = customtkinter.CTkLabel(self.weather_frame, text="",
                                                      font=("Helvetica", 18), text_color="#ECF0F1")
        self.condition_label.pack(pady=10)

        # Additional weather info
        self.additional_info = customtkinter.CTkLabel(self.weather_frame, text="",
                                                      font=("Helvetica", 14), text_color="#BDC3C7")
        self.additional_info.pack(pady=10)

        # Store the last fetched weather data
        self.last_weather_data = None

    def get_weather(self) -> None:
        """
        Fetches the weather data for the entered city using the OpenWeather API and updates the UI
        with the weather information. If the city is not found, displays an error message.
        """
        city: str = self.location_entry.get()
        if city:
            response_status, weather_data = self.weather_fetcher.fetch_weather_data(city)
            # If the request was successful, display the weather
            if response_status:
                self.last_weather_data = weather_data
                self.display_weather(weather_data)
            else:
                # Show the error and reset labels
                self.city_label.configure(text=weather_data.capitalize())
                self.temp_label.configure(text="")
                self.condition_label.configure(text="")
                self.additional_info.configure(text="")
                self.last_weather_data = None

    def display_weather(self, weather_data: dict) -> None:
        """
        Updates the UI with the fetched weather data.

        :param weather_data: A dictionary containing weather information such as temperature, condition,
                             feels_like temperature, min/max temperature, humidity, wind speed, and pressure.
        """
        self.city_label.configure(text=f"{weather_data['city']}, {weather_data['country']}")

        temp = weather_data['temperature']
        feels_like = weather_data['feels_like']
        temp_min = weather_data['temp_min']
        temp_max = weather_data['temp_max']
        wind_speed = weather_data['wind_speed']

        if not self.is_metric:
            temp = self.celsius_to_fahrenheit(temp)
            feels_like = self.celsius_to_fahrenheit(feels_like)
            temp_min = self.celsius_to_fahrenheit(temp_min)
            temp_max = self.celsius_to_fahrenheit(temp_max)
            wind_speed = self.mps_to_mph(wind_speed)

        unit = "°C" if self.is_metric else "°F"
        speed_unit = "m/s" if self.is_metric else "mph"

        self.temp_label.configure(text=f"{temp:.1f}{unit}")
        self.condition_label.configure(text=f"{weather_data['condition'].capitalize()}")
        self.additional_info.configure(text=(
            f"Feels like: {feels_like:.1f}{unit}  |  "
            f"Min: {temp_min:.1f}{unit}  |  Max: {temp_max:.1f}{unit}\n"
            f"Humidity: {weather_data['humidity']}%  |  Wind: {wind_speed:.1f} {speed_unit}, {weather_data['wind_deg']}°\n"
            f"Pressure: {weather_data['pressure']} hPa  |  Visibility: {weather_data['visibility'] / 1000:.1f} km"
        ))

    def toggle_units(self) -> None:
        """
        Toggles between metric (Celsius) and imperial (Fahrenheit) units and updates the display.
        """
        self.is_metric = not self.is_metric
        self.unit_switch.configure(text="Switch to °F" if self.is_metric else "Switch to °C")

        if self.last_weather_data:
            self.display_weather(self.last_weather_data)

    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """
        Converts Celsius to Fahrenheit.

        :param celsius: Temperature in Celsius
        :return: Temperature in Fahrenheit
        """
        return (celsius * 9/5) + 32

    @staticmethod
    def mps_to_mph(mps: float) -> float:
        """
        Converts meters per second to miles per hour.

        :param mps: Speed in meters per second
        :return: Speed in miles per hour
        """
        return mps * 2.23694


# Running the app
if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    app = PyCast()
    app.mainloop()
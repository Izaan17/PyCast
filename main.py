import customtkinter
import constants
from open_weather import OpenWeatherAPI


class PyCast(customtkinter.CTk):
    """
    PyCast is a simple weather application that fetches and displays weather information for a given location using
    the OpenWeather API.
    """
    def __init__(self, **kwargs) -> None:
        """
        Initializes the PyCast weather application.

        :param kwargs: Additional arguments passed to the CTk (customtkinter) parent class.
        """
        super().__init__(**kwargs)

        # OpenWeather API Handler
        self.weather_fetcher = OpenWeatherAPI(constants.API_KEY)

        self.title("PyCast Weather App")
        self.geometry("500x600")
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
                self.display_weather(weather_data)
            else:
                # Show the error and reset labels
                self.city_label.configure(text=weather_data.capitalize())
                self.temp_label.configure(text="")
                self.condition_label.configure(text="")
                self.additional_info.configure(text="")

    def display_weather(self, weather_data: dict) -> None:
        """
        Updates the UI with the fetched weather data.

        :param weather_data: A dictionary containing weather information such as temperature, condition,
                             feels_like temperature, min/max temperature, humidity, wind speed, and pressure.
        """
        self.city_label.configure(text=f"{weather_data['city']}, {weather_data['country']}")
        self.temp_label.configure(text=f"{weather_data['temperature']}°C")
        self.condition_label.configure(text=f"{weather_data['condition'].capitalize()}")
        self.additional_info.configure(text=(
            f"Feels like: {weather_data['feels_like']}°C  |  "
            f"Min: {weather_data['temp_min']}°C  |  Max: {weather_data['temp_max']}°C\n"
            f"Humidity: {weather_data['humidity']}%  |  Wind: {weather_data['wind_speed']} m/s, {weather_data['wind_deg']}°\n"
            f"Pressure: {weather_data['pressure']} hPa  |  Visibility: {weather_data['visibility'] / 1000} km"
        ))


# Running the app
if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    app = PyCast()
    app.mainloop()
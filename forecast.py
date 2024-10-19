import requests
import config

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather_forecast(city, api_key):
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

    response = requests.get(forecast_url)
    if response.status_code == 200:
        forecast_data = response.json()
        print(f"\nWeather Forecast for {city}:")
        
        # Iterate over the forecast data (taking every 8th entry, which is every 3 hours)
        for entry in forecast_data['list'][::8]:  # Adjust as necessary for the granularity you need
            forecast_time = entry['dt_txt']
            temp_kelvin = entry['main']['temp']
            humidity = entry['main']['humidity']
            wind_speed = entry['wind']['speed']
            main_weather = entry['weather'][0]['main']

            # Convert temperature
            temp_celsius = kelvin_to_celsius(temp_kelvin)

            print(f"{forecast_time} - Temp: {temp_celsius:.2f}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s, Condition: {main_weather}")
    else:
        print("Failed to retrieve forecast data:", response.status_code)

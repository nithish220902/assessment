import requests
import sqlite3
import time
from datetime import datetime
import config
import os
from forecast import get_weather_forecast

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

def save_city_to_config(city):
    with open('config.txt', 'w') as f:
        f.write(city)

def load_city_from_config():
    if os.path.exists('config.txt'):
        with open('config.txt', 'r') as f:
            city = f.read().strip()
            print(f"Loaded city from config: {city}")  # Debugging line
            return city
    return None  # Return None if the file doesn't exist

def get_city_choice():
    metros = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
    print("Select a city to fetch weather data:")
    for i, city in enumerate(metros, 1):
        print(f"{i}. {city}")
    choice = int(input("Enter the number of your choice: ")) - 1
    if 0 <= choice < len(metros):
        selected_city = metros[choice]
        save_city_to_config(selected_city)
        print(f"City selected: {selected_city}")
        return selected_city
    else:
        print("Invalid choice. Defaulting to Delhi.")
        default_city = 'Delhi'
        save_city_to_config(default_city)
        print(f"City selected: {default_city}")
        return default_city

def fetch_weather_data(selected_city):
    api_key = '9815ee4000d3928d11ad36adb41d3d78'  # Replace with your actual API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={api_key}"

    alert_threshold = 35.0
    consecutive_updates_needed = 2
    consecutive_count = 0

    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Create table for storing weather data if it doesn't exist
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            date TEXT,
            main TEXT,
            temp REAL,
            feels_like REAL,
            humidity REAL,
            wind_speed REAL,
            unit TEXT
        )
    ''')

    # Prompt for temperature unit
    unit = input("Enter preferred temperature unit (Celsius or Fahrenheit): ").strip().lower()
    if unit == 'celsius':
        unit_label = "°C"
    elif unit == 'fahrenheit':
        unit_label = "°F"
    else:
        print("Invalid unit entered. Defaulting to Celsius.")
        unit = 'celsius'
        unit_label = "°C"

    try:
        while True:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                temp_kelvin = data['main']['temp']
                feels_like_kelvin = data['main']['feels_like']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                main_weather = data['weather'][0]['main']

                # Convert temperature based on selected unit
                if unit == 'celsius':
                    temp = kelvin_to_celsius(temp_kelvin)
                    feels_like = kelvin_to_celsius(feels_like_kelvin)
                else:
                    temp = kelvin_to_fahrenheit(temp_kelvin)
                    feels_like = kelvin_to_fahrenheit(feels_like_kelvin)

                print(f"Weather data for {selected_city}")
                print("Main:", main_weather)
                print(f"Temperature: {temp:.2f}{unit_label}")
                print(f"Feels Like: {feels_like:.2f}{unit_label}")
                print(f"Humidity: {humidity}%")
                print(f"Wind Speed: {wind_speed} m/s")

                date = datetime.now().strftime("%Y-%m-%d")
                cursor.execute('''
                    INSERT INTO weather (city, date, main, temp, feels_like, humidity, wind_speed, unit)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (selected_city, date, main_weather, temp, feels_like, humidity, wind_speed, unit))
                conn.commit()
                print("Weather data saved to database.")

                if temp > alert_threshold:
                    consecutive_count += 1
                    print(f"Alert! Temperature exceeds {alert_threshold}°C. Count: {consecutive_count}")
                    if consecutive_count >= consecutive_updates_needed:
                        print(f"ALERT: The temperature in {selected_city} has exceeded {alert_threshold}°C for {consecutive_updates_needed} consecutive updates!")
                else:
                    consecutive_count = 0

                # Call the get_weather_forecast function
                get_weather_forecast(selected_city, api_key)

            else:
                print("Failed to retrieve data:", response.status_code)

            # Prompt the user if they want to stop
            user_input = input("Type 'stop' to end data fetching and proceed with visualization or press Enter to continue: ").strip().lower()
            if user_input == 'stop':
                print("Stopping weather data fetching.")
                break

            time.sleep(300)  # Sleep for 5 minutes

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    finally:
        conn.close()

def calculate_daily_summary(city, date):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT temp, main, humidity, wind_speed FROM weather 
        WHERE city = ? AND date = ?
    ''', (city, date))

    rows = cursor.fetchall()

    if not rows:
        print(f"No data available for {city} on {date}")
        conn.close()
        return

    temps = [row[0] for row in rows]
    conditions = [row[1] for row in rows]
    humidities = [row[2] for row in rows]
    wind_speeds = [row[3] for row in rows]

    average_temp = sum(temps) / len(temps)
    max_temp = max(temps)
    min_temp = min(temps)
    average_humidity = sum(humidities) / len(humidities)
    average_wind_speed = sum(wind_speeds) / len(wind_speeds)
    dominant_condition = max(set(conditions), key=conditions.count)

    print(f"Daily Weather Summary for {city} on {date}:")
    print(f"  Average Temperature: {average_temp:.2f}")
    print(f"  Maximum Temperature: {max_temp:.2f}")
    print(f"  Minimum Temperature: {min_temp:.2f}")
    print(f"  Average Humidity: {average_humidity:.2f}%")
    print(f"  Average Wind Speed: {average_wind_speed:.2f} m/s")
    print(f"  Dominant Weather Condition: {dominant_condition}")

    cursor.execute('''
        INSERT INTO daily_summary (city, date, average_temp, max_temp, min_temp, average_humidity, average_wind_speed, dominant_condition)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (city, date, average_temp, max_temp, min_temp, average_humidity, average_wind_speed, dominant_condition))

    conn.commit()
    print(f"Daily summary for {city} on {date} stored in the database.")
    conn.close()

if __name__ == "__main__":
    selected_city = load_city_from_config()  # Load selected city at the start
    if selected_city is None:
        selected_city = get_city_choice()  # Prompt for city selection if none is loaded
    else:
        print(f"Using previously selected city: {selected_city}")  # Debugging line
    fetch_weather_data(selected_city)  # Pass selected city to fetch_weather_data

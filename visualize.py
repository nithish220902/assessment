import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from weather_data import calculate_daily_summary
from datetime import datetime
import config
import os

# Add this function to visualize.py
def load_city_from_config():
    if os.path.exists('config.txt'):
        with open('config.txt', 'r') as f:
            config.selected_city = f.read().strip()

alert_threshold = 35.0  # Set the alert threshold used in your main code

def visualize_weather_data(city):
    city = config.selected_city
    conn = sqlite3.connect('weather_data.db')
    query = '''
        SELECT date, AVG(temp) as avg_temp, MAX(temp) as max_temp, MIN(temp) as min_temp,
               AVG(humidity) as avg_humidity, AVG(wind_speed) as avg_wind_speed
        FROM weather
        WHERE city = ?
        GROUP BY date
        ORDER BY date
    '''
    df = pd.read_sql_query(query, conn, params=(city,))
    conn.close()

    if df.empty:
        print(f"No weather data available for {city}.")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['avg_temp'], marker='o', label='Average Temp (°C)', color='blue')
    plt.plot(df['date'], df['avg_humidity'], marker='o', label='Average Humidity (%)', color='green')
    plt.plot(df['date'], df['avg_wind_speed'], marker='o', label='Average Wind Speed (m/s)', color='purple')

    alert_dates = get_alert_dates(city)
    for alert_date in alert_dates:
        plt.axvline(x=alert_date, color='orange', linestyle='--', label='Alert Triggered')

    plt.title(f"Weather Data for {city}")
    plt.xlabel("Date")
    plt.ylabel("Measurements")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


def get_alert_dates(city):
    city = config.selected_city
    # Connect to the SQLite database to retrieve alert dates
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Query to get dates where alerts were triggered
    cursor.execute('''
        SELECT date FROM weather
        WHERE city = ? AND temp > ?
    ''', (city, alert_threshold))  # Use the same alert_threshold from your main file

    alert_dates = [row[0] for row in cursor.fetchall()]

    conn.close()
    return alert_dates

def visualize_historical_trends():
    city = config.selected_city
    # Connect to the SQLite database
    conn = sqlite3.connect('weather_data.db')

    # Fetch historical temperature data over a longer period (e.g., month)
    query = '''
        SELECT date, AVG(temp) as avg_temp
        FROM weather
        WHERE city = ?
        GROUP BY date
        ORDER BY date
    '''
    df = pd.read_sql_query(query, conn, params=(city,))
    
    # Close the database connection
    conn.close()

    # Check if data is available
    if df.empty:
        print(f"No historical weather data available for {city}.")
        return

    # Plotting historical trends
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['avg_temp'], marker='o', label='Average Temperature', color='blue')

    plt.title(f"Historical Temperature Trends for {city}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    load_city_from_config()  # Load selected city at the start
    if config.selected_city is None:
        print("No city has been selected. Please run weather_data.py and select a city before running visualize.py.")
        exit()
    else:
        print(f"City for visualization: {config.selected_city}")

    # Set the date for which you want to generate the summary and visualization
    date = datetime.now().strftime('%Y-%m-%d')
    calculate_daily_summary(config.selected_city, date)  # Calculate daily summary for the selected city
    visualize_weather_data(config.selected_city)  # Pass the selected city to the function
    visualize_historical_trends()  # Call historical trends visualization
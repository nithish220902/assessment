# Weather Monitoring System

## Overview
The Weather Monitoring System is a real-time data processing application that retrieves weather data from the OpenWeatherMap API, stores it in a SQLite database, and provides users with the ability to visualize weather conditions and summaries. The application also includes alerting features for specified weather conditions.

## Features
- Retrieve current weather data for a specified city.
- Store weather data in a SQLite database.
- Calculate and store daily weather summaries (average, maximum, minimum temperatures, etc.).
- Set and trigger alerts for specified temperature thresholds.
- Generate weather forecasts for upcoming days.

## Technologies Used
- Python
- SQLite
- Requests library (for API calls)
- ConfigParser (for configuration management)

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)

### Dependencies
You need to install the following Python libraries to run the application:
- `requests`
- `sqlite3` (comes with Python)
- `matplotlib` (for data visualization)

### Steps to Set Up the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-github-username>/assessment.git
   cd assessment

### Install required dependencies
pip install -r requirements.txt

### The application will automatically create a database file named weather_data.db on the first run.

### Execute the following command to start fetching weather data
python weather_data.py

The application will prompt you to select a city and a preferred temperature unit (Celsius or Fahrenheit).
You can stop the data fetching at any time by typing 'stop' when prompted

### Note on City Selection for Graph Representation
For optimal graph representation and analysis, it is recommended to use Delhi or Mumbai as the selected city when running this weather monitoring application. The database contains a richer dataset for these cities over the past three days, resulting in more accurate and informative visualizations.

While the application is designed to work with any of the available cities (Chennai, Bangalore, Kolkata, and Hyderabad), please be aware that data for these cities may be limited. To obtain sufficient data for effective graph representation, you will need to run the code repeatedly over three days, collecting and storing the weather data for these cities.



### After collecting weather data, run the visualization script
python visualize.py

The script will generate visualizations similar to the following:

Temperature trend over the past week
Humidity and wind speed comparisons

### To run the test cases, use the following command
python test_weather_monitor.py

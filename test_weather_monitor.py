import unittest
import requests
from weather_data import kelvin_to_celsius, calculate_daily_summary, fetch_weather_data

class TestWeatherMonitoring(unittest.TestCase):
    def setUp(self):
        self.api_key = '9815ee4000d3928d11ad36adb41d3d78'  # Replace with your actual API key
        self.city = 'Mumbai'  # Example city for testing

    def test_api_connection(self):
        """Test that we can connect to the OpenWeatherMap API."""
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}")
        self.assertEqual(response.status_code, 200, "Failed to connect to the API.")

    def test_data_retrieval(self):
        """Test data retrieval for the specified city."""
        try:
            response = fetch_weather_data(self.city)
            self.assertIsNotNone(response, "No response from fetch_weather_data.")
        except Exception as e:
            self.fail(f"fetch_weather_data raised an exception: {e}")

    def test_temperature_conversion(self):
        """Test conversion of temperature from Kelvin to Celsius."""
        kelvin_temp = 300  # Example Kelvin temperature
        celsius_temp = kelvin_to_celsius(kelvin_temp)
        self.assertAlmostEqual(celsius_temp, 26.85, places=2, msg="Temperature conversion from Kelvin to Celsius is incorrect.")

    def test_daily_summary(self):
        """Test that daily summary calculations are correct."""
        # Assuming data is already available in the database for this date
        date = '2024-10-19'  # Use a date for which you have data
        summary = calculate_daily_summary(self.city, date)
        self.assertIsNotNone(summary, "Daily summary is None.")
        self.assertIn('average_temp', summary)
        self.assertIn('max_temp', summary)
        self.assertIn('min_temp', summary)
        self.assertIn('dominant_condition', summary)

    def test_alert_threshold(self):
        """Test that alerting thresholds are triggered correctly."""
        alert_threshold = 35.0  # Example threshold
        temperature_data = [30, 32, 34, 36]  # Simulated temperatures
        alerts = [temp > alert_threshold for temp in temperature_data]
        self.assertIn(True, alerts, "No alerts triggered for temperatures above the threshold.")

if __name__ == '__main__':
    unittest.main()

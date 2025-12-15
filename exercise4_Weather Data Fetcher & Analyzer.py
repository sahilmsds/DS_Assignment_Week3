import requests
import csv
from datetime import datetime, timezone

def fetch_weather(city: str, api_key: str) -> dict:
    """
    Fetch weather data for a given city using OpenWeatherMap API.
    Returns JSON response as a dictionary.
    Handles errors gracefully.
    """
    try:
        # API endpoint with city, API key, and units set to metric (Celsius)
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)  # Send GET request
        response.raise_for_status()   # Raise exception for HTTP errors (4xx, 5xx)

        # Parse JSON response to dict and return
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors such as 404 for invalid city
        print(f"HTTP error occurred: {http_err}")
        return {}
    except requests.exceptions.RequestException as req_err:
        # Handle other request exceptions (network issues, timeouts)
        print(f"Network error occurred: {req_err}")
        return {}

def analyze_weather(weather_data: dict) -> str:
    """
    Analyze the weather data and return a summary string.
    Temperature categories:
        Cold (≤10°C), Mild (11-24°C), Hot (≥25°C)
    Adds warnings for:
        Wind speed > 10 m/s, Humidity > 80%
    """
    if not weather_data or 'main' not in weather_data or 'wind' not in weather_data:
        return "No valid weather data available."

    temp = weather_data['main']['temp']      # Current temperature in Celsius
    wind_speed = weather_data['wind']['speed']  # Wind speed in m/s
    humidity = weather_data['main']['humidity'] # Humidity in percentage

    # Determine temperature category
    if temp <= 10:
        temp_desc = "Cold (≤10°C)"
    elif 11 <= temp <= 24:
        temp_desc = "Mild (11-24°C)"
    else:
        temp_desc = "Hot (≥25°C)"

    # Prepare warning messages if conditions met
    warnings = []
    if wind_speed > 10:
        warnings.append("High wind alert!")
    if humidity > 80:
        warnings.append("Humid conditions!")

    # Combine summary and warnings
    summary = temp_desc
    if warnings:
        summary += " " + " ".join(warnings)

    return summary

def log_weather(city: str, filename: str, api_key: str):
    """
    Fetch weather data for the city, analyze it, and append the data to a CSV file.
    CSV format columns: datetime, city, temperature, wind_speed, humidity, summary
    """
    weather_data = fetch_weather(city, api_key)  # Fetch weather data
    if not weather_data:
        print("Failed to fetch weather data. Logging aborted.")
        return
    
    temp = weather_data['main'].get('temp', '')
    wind_speed = weather_data['wind'].get('speed', '')
    humidity = weather_data['main'].get('humidity', '')
    summary = analyze_weather(weather_data)

    timestamp = datetime.now(timezone.utc).isoformat()

    row = [timestamp, city, temp, wind_speed, humidity, summary]

    try:
        with open(filename, 'r') as file:
            first_char = file.read(1)
    except FileNotFoundError:
        first_char = ''

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
  
        if first_char == '':
            writer.writerow(["datetime", "city", "temperature(C)", "wind_speed(m/s)", "humidity(%)", "summary"])

        writer.writerow(row)

    print(f"Logged weather data for {city} to {filename}")

if __name__ == "__main__":
    API_KEY = "fa2c3c311a67da31cfca5cf0347baadd"
    city_name = "London"
    filename = "weather_log.csv"

    data = fetch_weather(city_name, API_KEY)
    print(data)

    print(analyze_weather(data))

    log_weather(city_name, filename, API_KEY)

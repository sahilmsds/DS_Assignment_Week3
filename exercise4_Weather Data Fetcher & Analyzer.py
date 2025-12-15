import os
import requests
import csv
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise ValueError("Please set the environment variable OPENWEATHER_API_KEY")

def fetch_weather(city: str, api_key: str) -> dict:
    """
    Fetch weather data for a given city using OpenWeatherMap API.
    Returns JSON response as a dictionary.
    Handles errors gracefully.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {}
    except requests.exceptions.RequestException as req_err:
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

    temp = weather_data['main']['temp']
    wind_speed = weather_data['wind']['speed']
    humidity = weather_data['main']['humidity']

    if temp <= 10:
        temp_desc = "Cold (≤10°C)"
    elif 11 <= temp <= 24:
        temp_desc = "Mild (11-24°C)"
    else:
        temp_desc = "Hot (≥25°C)"

    warnings = []
    if wind_speed > 10:
        warnings.append("High wind alert!")
    if humidity > 80:
        warnings.append("Humid conditions!")

    summary = temp_desc
    if warnings:
        summary += " " + " ".join(warnings)

    return summary

def log_weather(city: str, filename: str, api_key: str):
    """
    Fetch weather data for the city, analyze it, and append the data to a CSV file.
    CSV columns: datetime, city, temperature, wind_speed, humidity, summary
    """
    weather_data = fetch_weather(city, api_key)
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
    city_name = "London"
    filename = "weather_log.csv"

    data = fetch_weather(city_name, API_KEY)
    print(data)

    print(analyze_weather(data))

    log_weather(city_name, filename, API_KEY)

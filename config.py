import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Weather API Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
WEATHER_API_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Location Configuration (you can change these to your location)
CITY = os.getenv('CITY', 'New York')
COUNTRY_CODE = os.getenv('COUNTRY_CODE', 'US')

# Email Configuration (for Gmail)
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')  # App password for Gmail
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', '')

# Notification Settings
TEMPERATURE_THRESHOLD = 80  # Fahrenheit
CHECK_INTERVAL_MINUTES = 30  # How often to check weather

# Weather conditions that indicate rain
RAIN_CONDITIONS = [
    'rain', 'drizzle', 'thunderstorm', 'snow', 'sleet', 'shower rain'
] 
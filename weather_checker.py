import requests
import json
import pytz
from datetime import datetime
from config import WEATHER_API_KEY, WEATHER_API_BASE_URL, CITY, COUNTRY_CODE, TEMPERATURE_THRESHOLD, RAIN_CONDITIONS

class WeatherChecker:
    def __init__(self):
        self.api_key = WEATHER_API_KEY
        self.base_url = WEATHER_API_BASE_URL
        
    def get_weather_data(self):
        """Fetch current weather data from OpenWeatherMap API"""
        if not self.api_key:
            raise ValueError("Weather API key not found. Please set WEATHER_API_KEY in your .env file")
        
        params = {
            'q': f"{CITY},{COUNTRY_CODE}",
            'appid': self.api_key,
            'units': 'imperial'  # Use Fahrenheit
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def get_weather_data_for_location(self, city, country_code):
        """Fetch current weather data for a specific location"""
        if not self.api_key:
            raise ValueError("Weather API key not found. Please set WEATHER_API_KEY in your .env file")
        
        params = {
            'q': f"{city},{country_code}",
            'appid': self.api_key,
            'units': 'imperial'  # Use Fahrenheit
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data for {city}: {e}")
            return None
    
    def get_forecast_data_for_location(self, city, country_code):
        """Fetch 5-day forecast data for a specific location"""
        if not self.api_key:
            raise ValueError("Weather API key not found. Please set WEATHER_API_KEY in your .env file")
        
        # Use the forecast API endpoint
        forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        
        params = {
            'q': f"{city},{country_code}",
            'appid': self.api_key,
            'units': 'imperial'  # Use Fahrenheit
        }
        
        try:
            response = requests.get(forecast_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data for {city}: {e}")
            return None
    
    def get_location_timezone(self, weather_data):
        """Get timezone information from weather data"""
        if not weather_data or 'timezone' not in weather_data:
            return None
        
        timezone_offset = weather_data['timezone']  # Offset in seconds from UTC
        
        # Convert offset to timezone name
        offset_hours = timezone_offset // 3600
        
        # Common timezone mappings based on offset
        timezone_map = {
            -12: 'Pacific/Kwajalein',
            -11: 'Pacific/Midway',
            -10: 'Pacific/Honolulu',
            -9: 'America/Anchorage',
            -8: 'America/Los_Angeles',
            -7: 'America/Denver',
            -6: 'America/Chicago',
            -5: 'America/New_York',
            -4: 'America/Halifax',
            -3: 'America/Sao_Paulo',
            -2: 'Atlantic/South_Georgia',
            -1: 'Atlantic/Azores',
            0: 'UTC',
            1: 'Europe/London',
            2: 'Europe/Paris',
            3: 'Europe/Moscow',
            4: 'Asia/Dubai',
            5: 'Asia/Kolkata',
            6: 'Asia/Dhaka',
            7: 'Asia/Bangkok',
            8: 'Asia/Shanghai',
            9: 'Asia/Tokyo',
            10: 'Australia/Sydney',
            11: 'Pacific/Guadalcanal',
            12: 'Pacific/Auckland'
        }
        
        return timezone_map.get(offset_hours, 'UTC')
    
    def is_8am_in_location(self, weather_data):
        """Check if it's 8:00 AM in the location's timezone"""
        if not weather_data:
            return False
        
        timezone_name = self.get_location_timezone(weather_data)
        if not timezone_name:
            return False
        
        try:
            # Get current time in the location's timezone
            tz = pytz.timezone(timezone_name)
            local_time = datetime.now(tz)
            
            # Check if it's 8:00 AM
            return local_time.hour == 8 and local_time.minute == 0
        except Exception as e:
            print(f"Error checking timezone for location: {e}")
            return False
    
    def analyze_weather(self, weather_data, forecast_data=None):
        """Analyze weather data and return notification recommendations"""
        if not weather_data:
            return None
        
        try:
            current_temp = weather_data['main']['temp']
            weather_condition = weather_data['weather'][0]['main'].lower()
            weather_description = weather_data['weather'][0]['description'].lower()
            
            notifications = []
            
            # Check for rain conditions (current weather)
            is_rainy = any(condition in weather_description for condition in RAIN_CONDITIONS)
            if is_rainy:
                notifications.append("🌧️ Bring an umbrella! Rain is expected.")
            
            # Get daily high temperature from forecast if available
            daily_high = current_temp  # Default to current temp
            if forecast_data and 'list' in forecast_data:
                daily_high = self._get_daily_high_temperature(forecast_data)
            
            # Check for high temperature using daily high
            if daily_high > TEMPERATURE_THRESHOLD:
                if is_rainy:
                    notifications.append("☀️🌧️ High temperature and rain expected. Bring umbrella AND sunscreen!")
                else:
                    notifications.append("☀️ High temperature expected. Don't forget sunscreen!")
            
            return {
                'current_temperature': current_temp,
                'daily_high': daily_high,
                'condition': weather_condition,
                'description': weather_description,
                'notifications': notifications,
                'location': f"{CITY}, {COUNTRY_CODE}"
            }
            
        except KeyError as e:
            print(f"Error parsing weather data: {e}")
            return None
    
    def _get_daily_high_temperature(self, forecast_data):
        """Extract the daily high temperature from forecast data"""
        try:
            # Get today's date
            today = datetime.now().date()
            
            # Find the highest temperature for today
            daily_high = -999  # Start with very low temp
            
            for item in forecast_data['list']:
                # Parse the forecast time
                forecast_time = datetime.fromtimestamp(item['dt'])
                forecast_date = forecast_time.date()
                
                # Only consider today's forecasts
                if forecast_date == today:
                    temp = item['main']['temp']
                    if temp > daily_high:
                        daily_high = temp
            
            # If no forecast found for today, return a reasonable default
            if daily_high == -999:
                return 75  # Default temperature
            
            return daily_high
            
        except Exception as e:
            print(f"Error getting daily high temperature: {e}")
            return 75  # Default temperature
    
    def should_send_notification(self, weather_analysis):
        """Determine if a notification should be sent"""
        return weather_analysis and len(weather_analysis['notifications']) > 0 
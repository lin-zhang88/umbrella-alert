#!/usr/bin/env python3
"""
Test script to verify timezone-aware weather checking
"""

from weather_checker import WeatherChecker
import pytz
from datetime import datetime

def test_timezone_functionality():
    """Test timezone detection for different cities"""
    print("🌍 Testing Timezone-Aware Weather Checking")
    print("=" * 50)
    
    weather_checker = WeatherChecker()
    weather_checker.api_key = '56d2e99920ceb5470ea88d9105b886dc'
    
    # Test cities in different timezones
    test_cities = [
        ("New York", "US"),
        ("Los Angeles", "US"),
        ("London", "GB"),
        ("Tokyo", "JP"),
        ("Sydney", "AU"),
        ("Mumbai", "IN")
    ]
    
    for city, country in test_cities:
        print(f"\n📍 Testing {city}, {country}:")
        
        try:
            # Get weather data
            weather_data = weather_checker.get_weather_data_for_location(city, country)
            if weather_data:
                # Get timezone
                timezone_name = weather_checker.get_location_timezone(weather_data)
                if timezone_name:
                    # Get current time in that timezone
                    tz = pytz.timezone(timezone_name)
                    local_time = datetime.now(tz)
                    
                    # Check if it's 8:00 AM
                    is_8am = weather_checker.is_8am_in_location(weather_data)
                    
                    print(f"   🌐 Timezone: {timezone_name}")
                    print(f"   🕐 Local time: {local_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"   ⏰ Is 8:00 AM? {'✅ Yes' if is_8am else '❌ No'}")
                    
                    # Show weather info
                    if 'main' in weather_data and 'weather' in weather_data:
                        temp = weather_data['main']['temp']
                        condition = weather_data['weather'][0]['description']
                        print(f"   🌡️ Temperature: {temp:.1f}°F")
                        print(f"   ☁️ Condition: {condition}")
                else:
                    print(f"   ❌ Could not determine timezone")
            else:
                print(f"   ❌ Could not fetch weather data")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📋 Timezone-Aware Features:")
    print("• Each subscriber gets notifications at their local 8:00 AM")
    print("• System automatically detects timezone from weather API")
    print("• No more timezone confusion!")
    print("• Perfect for global users")

if __name__ == "__main__":
    test_timezone_functionality()

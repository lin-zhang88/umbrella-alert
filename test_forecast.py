#!/usr/bin/env python3
"""
Test script to verify forecast-based daily high temperature functionality
"""

from weather_checker import WeatherChecker
from datetime import datetime

def test_forecast_functionality():
    """Test forecast data and daily high temperature detection"""
    print("🔥 Testing Forecast-Based Daily High Temperature")
    print("=" * 55)
    
    weather_checker = WeatherChecker()
    weather_checker.api_key = '56d2e99920ceb5470ea88d9105b886dc'
    
    # Test cities
    test_cities = [
        ("Nashville", "US"),
        ("Los Angeles", "US"),
        ("Miami", "US"),
        ("Phoenix", "US")
    ]
    
    for city, country in test_cities:
        print(f"\n📍 Testing {city}, {country}:")
        
        try:
            # Get current weather
            weather_data = weather_checker.get_weather_data_for_location(city, country)
            if weather_data:
                current_temp = weather_data['main']['temp']
                print(f"   🌡️ Current Temperature: {current_temp:.1f}°F")
                
                # Get forecast data
                forecast_data = weather_checker.get_forecast_data_for_location(city, country)
                if forecast_data:
                    # Get daily high
                    daily_high = weather_checker._get_daily_high_temperature(forecast_data)
                    print(f"   🔥 Daily High: {daily_high:.1f}°F")
                    
                    # Analyze weather with forecast
                    weather_analysis = weather_checker.analyze_weather(weather_data, forecast_data)
                    if weather_analysis:
                        print(f"   📊 Analysis Results:")
                        print(f"      Current: {weather_analysis['current_temperature']:.1f}°F")
                        print(f"      Daily High: {weather_analysis['daily_high']:.1f}°F")
                        
                        # Check for alerts
                        if weather_analysis['notifications']:
                            print(f"   ⚠️ Alerts:")
                            for alert in weather_analysis['notifications']:
                                print(f"      {alert}")
                        else:
                            print(f"   ✅ No alerts needed")
                    
                    # Show forecast details
                    print(f"   📅 Forecast Details:")
                    today = datetime.now().date()
                    today_forecasts = []
                    
                    for item in forecast_data['list'][:8]:  # First 8 forecasts (24 hours)
                        forecast_time = datetime.fromtimestamp(item['dt'])
                        forecast_date = forecast_time.date()
                        
                        if forecast_date == today:
                            temp = item['main']['temp']
                            time_str = forecast_time.strftime('%H:%M')
                            today_forecasts.append(f"{time_str}: {temp:.1f}°F")
                    
                    if today_forecasts:
                        print(f"      Today's temperatures: {', '.join(today_forecasts[:4])}")
                    
                else:
                    print(f"   ❌ Could not fetch forecast data")
            else:
                print(f"   ❌ Could not fetch weather data")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📋 Forecast-Based Features:")
    print("• Uses 5-day forecast to get daily high temperature")
    print("• Sunscreen alerts based on hottest time of day")
    print("• More accurate than current temperature only")
    print("• Better planning for outdoor activities")

if __name__ == "__main__":
    test_forecast_functionality()

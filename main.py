#!/usr/bin/env python3
"""
Weather Notification System
Checks weather conditions and sends notifications for umbrella and sunscreen reminders
"""

import time
import schedule
from datetime import datetime
from weather_checker import WeatherChecker
from notification_sender import NotificationSender
from config import CHECK_INTERVAL_MINUTES

class WeatherNotificationSystem:
    def __init__(self):
        self.weather_checker = WeatherChecker()
        self.notification_sender = NotificationSender()
        self.last_notification_time = None
        
    def check_weather_and_notify(self):
        """Main function to check weather and send notifications if needed"""
        print(f"\n🌤️ Checking weather at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Get weather data
            weather_data = self.weather_checker.get_weather_data()
            if not weather_data:
                print("❌ Failed to fetch weather data")
                return
            
            # Get forecast data for daily high temperature
            forecast_data = self.weather_checker.get_forecast_data_for_location(CITY, COUNTRY_CODE)
            
            # Analyze weather conditions
            weather_analysis = self.weather_checker.analyze_weather(weather_data, forecast_data)
            if not weather_analysis:
                print("❌ Failed to analyze weather data")
                return
            
            # Display current weather
            print(f"📍 Location: {weather_analysis['location']}")
            print(f"🌡️ Current Temperature: {weather_analysis['current_temperature']:.1f}°F")
            print(f"🔥 Daily High: {weather_analysis['daily_high']:.1f}°F")
            print(f"☁️ Condition: {weather_analysis['description'].title()}")
            
            # Check if notification should be sent
            if self.weather_checker.should_send_notification(weather_analysis):
                print("⚠️ Weather alerts detected!")
                for notification in weather_analysis['notifications']:
                    print(f"   {notification}")
                
                # Send notification
                if self.notification_sender.send_email_notification(weather_analysis):
                    self.last_notification_time = datetime.now()
                    print("✅ Notification sent successfully!")
                else:
                    print("❌ Failed to send notification")
            else:
                print("✅ No weather alerts - you're all set!")
                
        except Exception as e:
            print(f"❌ Error in weather check: {e}")
    
    def run_once(self):
        """Run the weather check once"""
        self.check_weather_and_notify()
    
    def run_scheduled(self):
        """Run the weather check on a schedule"""
        print(f"🚀 Starting Weather Notification System")
        print(f"⏰ Checking weather every {CHECK_INTERVAL_MINUTES} minutes")
        print(f"📍 Location: {self.weather_checker.get_weather_data()['name'] if self.weather_checker.get_weather_data() else 'Unknown'}")
        print("Press Ctrl+C to stop the application\n")
        
        # Schedule the job
        schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(self.check_weather_and_notify)
        
        # Run immediately once
        self.check_weather_and_notify()
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute for scheduled tasks
        except KeyboardInterrupt:
            print("\n👋 Weather Notification System stopped by user")

def main():
    """Main entry point"""
    print("🌤️ Weather Notification System")
    print("=" * 40)
    
    # Initialize the system
    weather_system = WeatherNotificationSystem()
    
    # Check if we have the required configuration
    try:
        # Test weather API
        test_data = weather_system.weather_checker.get_weather_data()
        if not test_data:
            print("❌ Cannot connect to weather API. Please check your API key.")
            return
        
        print("✅ Weather API connection successful!")
        
        # Test email configuration
        if weather_system.notification_sender.email_address:
            print("📧 Email configuration found")
        else:
            print("⚠️ Email configuration not found. Notifications will be disabled.")
        
        print("\nChoose an option:")
        print("1. Run once (check weather now)")
        print("2. Run scheduled (check every 30 minutes)")
        print("3. Send test email")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            weather_system.run_once()
        elif choice == "2":
            weather_system.run_scheduled()
        elif choice == "3":
            if weather_system.notification_sender.send_test_email():
                print("✅ Test email sent successfully!")
            else:
                print("❌ Failed to send test email")
        elif choice == "4":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice. Please run the program again.")
            
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main() 
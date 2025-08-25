#!/usr/bin/env python3
"""
Weather Notification Web App
Flask web application for users to subscribe to weather notifications
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime
import pytz
from weather_checker import WeatherChecker
from notification_sender import NotificationSender
from config import EMAIL_ADDRESS, EMAIL_PASSWORD
import threading
import time

app = Flask(__name__)
app.secret_key = 'weather_notification_secret_key_2024'

# Database setup
def init_db():
    """Initialize the database with subscribers table"""
    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='subscribers'")
    table_exists = cursor.fetchone() is not None
    
    if not table_exists:
        # Create new table with zipcode
        cursor.execute('''
            CREATE TABLE subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                city TEXT NOT NULL,
                zipcode TEXT,
                country_code TEXT NOT NULL,
                subscribed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_notification TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
    else:
        # Check if zipcode column exists
        cursor.execute("PRAGMA table_info(subscribers)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'zipcode' not in columns:
            # Add zipcode column to existing table
            cursor.execute('ALTER TABLE subscribers ADD COLUMN zipcode TEXT')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def index():
    """Main page with subscription form"""
    return render_template('index.html')

@app.route('/check_subscription', methods=['POST'])
def check_subscription():
    """Check if an email is already subscribed"""
    email = request.form.get('email')
    
    if not email:
        return jsonify({'error': 'Please provide an email address'})
    
    try:
        conn = sqlite3.connect('subscribers.db')
        cursor = conn.cursor()
        cursor.execute('SELECT email, city, zipcode, is_active FROM subscribers WHERE email = ?', (email,))
        subscriber = cursor.fetchone()
        conn.close()
        
        if subscriber:
            email, city, zipcode, is_active = subscriber
            location = city
            if zipcode:
                location = f"{city}, {zipcode}"
            
            if is_active:
                return jsonify({
                    'subscribed': True,
                    'location': location,
                    'message': f'You are already subscribed to weather alerts for {location}.'
                })
            else:
                return jsonify({
                    'subscribed': False,
                    'location': location,
                    'message': f'You were previously subscribed to {location} but are currently unsubscribed.'
                })
        else:
            return jsonify({
                'subscribed': False,
                'message': 'Email not found in our subscription list.'
            })
            
    except Exception as e:
        return jsonify({'error': f'Error checking subscription: {str(e)}'})

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Handle new subscription"""
    email = request.form.get('email')
    city = request.form.get('city')
    zipcode = request.form.get('zipcode', '').strip()
    country_code = request.form.get('country_code', 'US')
    
    if not email or not city:
        flash('Please provide both email and city!', 'error')
        return redirect(url_for('index'))
    
    try:
        # Test the location with weather API
        weather_checker = WeatherChecker()
        weather_checker.api_key = '56d2e99920ceb5470ea88d9105b886dc'  # Your API key
        weather_checker.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Build location string (city + zipcode if provided)
        location = city
        if zipcode:
            location = f"{city}, {zipcode}"
        
        # Test location
        test_data = weather_checker.get_weather_data_for_location(location, country_code)
        if not test_data:
            flash(f'Could not find weather data for {location}, {country_code}. Please check the city name and zipcode.', 'error')
            return redirect(url_for('index'))
        
        # Check if email already exists
        conn = sqlite3.connect('subscribers.db')
        cursor = conn.cursor()
        cursor.execute('SELECT email, city, zipcode FROM subscribers WHERE email = ?', (email,))
        existing_subscriber = cursor.fetchone()
        
        if existing_subscriber:
            # Email already exists - update their location
            existing_email, existing_city, existing_zipcode = existing_subscriber
            cursor.execute('''
                UPDATE subscribers 
                SET city = ?, zipcode = ?, country_code = ?, subscribed_date = ?, is_active = 1
                WHERE email = ?
            ''', (city, zipcode, country_code, datetime.now(), email))
            conn.commit()
            conn.close()
            
            # Send welcome email for the updated location
            email_sent = send_welcome_email(email, location, country_code)
            
            if email_sent:
                flash(f'Updated your subscription! You are now subscribed to weather alerts for {location}. Welcome email sent!', 'success')
            else:
                flash(f'Updated your subscription! You are now subscribed to weather alerts for {location}. (Email notifications not configured)', 'success')
        else:
            # New subscriber - insert new record
            cursor.execute('''
                INSERT INTO subscribers (email, city, zipcode, country_code, subscribed_date, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (email, city, zipcode, country_code, datetime.now(), True))
            conn.commit()
            conn.close()
            
            # Send welcome email
            email_sent = send_welcome_email(email, location, country_code)
            
            if email_sent:
                flash(f'Successfully subscribed to weather alerts for {location}! Welcome email sent!', 'success')
            else:
                flash(f'Successfully subscribed to weather alerts for {location}! (Email notifications not configured)', 'success')
        
    except Exception as e:
        flash(f'Error subscribing: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """Handle unsubscription"""
    email = request.form.get('email')
    
    if not email:
        flash('Please provide an email address to unsubscribe.', 'error')
        return redirect(url_for('index'))
    
    try:
        conn = sqlite3.connect('subscribers.db')
        cursor = conn.cursor()
        
        # Check if email exists
        cursor.execute('SELECT email, city FROM subscribers WHERE email = ?', (email,))
        existing_subscriber = cursor.fetchone()
        
        if existing_subscriber:
            # Email exists - deactivate subscription
            cursor.execute('UPDATE subscribers SET is_active = 0 WHERE email = ?', (email,))
            conn.commit()
            conn.close()
            flash(f'Successfully unsubscribed {email} from weather notifications.', 'success')
        else:
            # Email doesn't exist
            conn.close()
            flash(f'Email {email} was not found in our subscription list.', 'error')
    
    except Exception as e:
        flash(f'Error unsubscribing: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    """Admin page to view subscribers and send test notifications"""
    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, city, zipcode, country_code, subscribed_date, last_notification, is_active FROM subscribers WHERE is_active = 1 ORDER BY subscribed_date DESC')
    subscribers = cursor.fetchall()
    conn.close()
    
    return render_template('admin.html', subscribers=subscribers)

@app.route('/send_test', methods=['POST'])
def send_test():
    """Send test notification to all subscribers"""
    try:
        send_notifications_to_all()
        flash('Test notifications sent to all active subscribers!', 'success')
    except Exception as e:
        flash(f'Error sending notifications: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

def send_welcome_email(email, city, country_code):
    """Send welcome email to new subscriber"""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print(f"⚠️ Email configuration not set up - welcome email not sent to {email}")
        print(f"📧 Would have sent welcome email to {email} for {city}, {country_code}")
        print(f"🔧 To enable email notifications, set up EMAIL_ADDRESS and EMAIL_PASSWORD in .env file")
        return False
    
    try:
        notification_sender = NotificationSender()
        notification_sender.recipient_email = email
        
        welcome_data = {
            'location': f"{city}, {country_code}",
            'current_temperature': 75.0,
            'daily_high': 75.0,
            'description': 'welcome',
            'notifications': [
                f'🎉 Welcome to UmbrellaAlert!',
                f'📍 You will receive daily weather alerts for {city}, {country_code}',
                f'🌧️ Umbrella alerts when rain is expected',
                f'☀️ Sunscreen alerts when temperature > 80°F',
                f'⏰ Daily checks at 8:00 AM in your local timezone',
                f'📧 You will only receive emails when alerts are needed!'
            ]
        }
        
        success = notification_sender.send_email_notification(welcome_data)
        if success:
            print(f"✅ Welcome email sent to {email}")
        else:
            print(f"❌ Failed to send welcome email to {email}")
        return success
        
    except Exception as e:
        print(f"❌ Error sending welcome email to {email}: {e}")
        return False

def send_notifications_to_all():
    """Send weather notifications to all active subscribers - only when alerts are needed"""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("⚠️ Email configuration not set up - notifications disabled")
        return
    
    weather_checker = WeatherChecker()
    notification_sender = NotificationSender()
    
    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email, city, zipcode, country_code FROM subscribers WHERE is_active = 1')
    subscribers = cursor.fetchall()
    conn.close()
    
    print(f"🔍 Checking weather for {len(subscribers)} active subscribers...")
    
    notifications_sent = 0
    for email, city, zipcode, country_code in subscribers:
        try:
            # Build location string (city + zipcode if provided)
            location = city
            if zipcode:
                location = f"{city}, {zipcode}"
            
            # Get weather for this subscriber's location
            weather_data = weather_checker.get_weather_data_for_location(location, country_code)
            if weather_data:
                weather_analysis = weather_checker.analyze_weather(weather_data)
                
                # Only send notification if alerts are needed
                if weather_analysis and weather_checker.should_send_notification(weather_analysis):
                    # Update recipient email temporarily
                    notification_sender.recipient_email = email
                    
                    if notification_sender.send_email_notification(weather_analysis):
                        # Update last notification time
                        conn = sqlite3.connect('subscribers.db')
                        cursor = conn.cursor()
                        cursor.execute('UPDATE subscribers SET last_notification = ? WHERE email = ?', 
                                     (datetime.now(), email))
                        conn.commit()
                        conn.close()
                        
                        print(f"✅ Alert sent to {email} for {city}: {weather_analysis['notifications']}")
                        notifications_sent += 1
                    else:
                        print(f"❌ Failed to send alert to {email} for {city}")
                else:
                    print(f"ℹ️ No alerts needed for {email} in {city} - weather is good!")
                    
        except Exception as e:
            print(f"❌ Error checking weather for {email} in {city}: {e}")
    
    print(f"📊 Daily weather check completed: {notifications_sent} alerts sent out of {len(subscribers)} subscribers")

def background_notification_service():
    """Background service to send notifications daily at 8:00 AM in each location's timezone"""
    while True:
        try:
            # Check weather for all subscribers based on their local timezone
            check_weather_for_all_timezones()
            
            # Wait 1 minute before next check
            time.sleep(60)
                
        except Exception as e:
            print(f"Background notification error: {e}")
            time.sleep(60)

def check_weather_for_all_timezones():
    """Check weather for all subscribers based on their local 8:00 AM"""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("⚠️ Email configuration not set up - notifications disabled")
        return
    
    weather_checker = WeatherChecker()
    notification_sender = NotificationSender()
    
    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email, city, zipcode, country_code FROM subscribers WHERE is_active = 1')
    subscribers = cursor.fetchall()
    conn.close()
    
    if not subscribers:
        return
    
    print(f"🌍 Checking weather for {len(subscribers)} subscribers across different timezones...")
    
    notifications_sent = 0
    for email, city, zipcode, country_code in subscribers:
        try:
            # Build location string (city + zipcode if provided)
            location = city
            if zipcode:
                location = f"{city}, {zipcode}"
            
            # Get weather for this subscriber's location
            weather_data = weather_checker.get_weather_data_for_location(location, country_code)
            if weather_data:
                # Check if it's 8:00 AM in this location's timezone
                if weather_checker.is_8am_in_location(weather_data):
                    print(f"🌅 8:00 AM in {location} - checking weather for {email}")
                    
                    # Get forecast data for daily high temperature
                    forecast_data = weather_checker.get_forecast_data_for_location(location, country_code)
                    
                    weather_analysis = weather_checker.analyze_weather(weather_data, forecast_data)
                    
                    # Only send notification if alerts are needed
                    if weather_analysis and weather_checker.should_send_notification(weather_analysis):
                        # Update recipient email temporarily
                        notification_sender.recipient_email = email
                        
                        if notification_sender.send_email_notification(weather_analysis):
                            # Update last notification time
                            conn = sqlite3.connect('subscribers.db')
                            cursor = conn.cursor()
                            cursor.execute('UPDATE subscribers SET last_notification = ? WHERE email = ?', 
                                         (datetime.now(), email))
                            conn.commit()
                            conn.close()
                            
                            print(f"✅ Alert sent to {email} for {city}: {weather_analysis['notifications']}")
                            notifications_sent += 1
                        else:
                            print(f"❌ Failed to send alert to {email} for {city}")
                    else:
                        print(f"ℹ️ No alerts needed for {email} in {city} - weather is good!")
                else:
                    # Not 8:00 AM in this location yet
                    timezone_name = weather_checker.get_location_timezone(weather_data)
                    if timezone_name:
                        tz = pytz.timezone(timezone_name)
                        local_time = datetime.now(tz)
                        print(f"⏰ {city} ({timezone_name}): {local_time.strftime('%H:%M')} - not 8:00 AM yet")
                    
        except Exception as e:
            print(f"❌ Error checking weather for {email} in {city}: {e}")
    
    if notifications_sent > 0:
        print(f"📊 Timezone-aware check completed: {notifications_sent} alerts sent")

if __name__ == '__main__':
    # Start background notification service in a separate thread
    notification_thread = threading.Thread(target=background_notification_service, daemon=True)
    notification_thread.start()
    
    print("☔ UmbrellaAlert Web App Starting...")
    print("📍 Web interface: http://localhost:5001")
    print("🔧 Admin panel: http://localhost:5001/admin")
    print("⏰ Background notifications: Daily at 8:00 AM")
    
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)

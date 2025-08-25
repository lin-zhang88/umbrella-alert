import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_EMAIL

class NotificationSender:
    def __init__(self):
        self.email_address = EMAIL_ADDRESS
        self.email_password = EMAIL_PASSWORD
        self.recipient_email = RECIPIENT_EMAIL
        
    def send_email_notification(self, weather_analysis):
        """Send email notification with weather alerts"""
        if not all([self.email_address, self.email_password, self.recipient_email]):
            print("Email configuration incomplete. Please check your .env file.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = self.recipient_email
            msg['Subject'] = f"☔ UmbrellaAlert - Weather Update for {weather_analysis['location']}"
            
            # Create email body
            body = self._create_email_body(weather_analysis)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_address, self.email_password)
            
            text = msg.as_string()
            server.sendmail(self.email_address, self.recipient_email, text)
            server.quit()
            
            print(f"✅ Weather notification sent successfully to {self.recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email notification: {e}")
            return False
    
    def _create_email_body(self, weather_analysis):
        """Create HTML email body with weather information"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if this is a welcome email (has 'welcome' in description)
        is_welcome = weather_analysis.get('description') == 'welcome'
        
        if is_welcome:
            # Welcome email template
            html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #f0f8ff; padding: 15px; border-radius: 5px; }}
                    .welcome {{ background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                    .footer {{ color: #666; font-size: 12px; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>🎉 Welcome to UmbrellaAlert!</h2>
                    <p><strong>Location:</strong> {weather_analysis['location']}</p>
                    <p><strong>Time:</strong> {current_time}</p>
                </div>
                
                <div class="welcome">
                    <h3>📧 What to Expect:</h3>
                    <ul>
            """
            
            for notification in weather_analysis['notifications']:
                html_body += f"<li>{notification}</li>"
            
            html_body += f"""
                    </ul>
                </div>
                
                <div class="footer">
                    <p>You're all set! You'll receive daily weather alerts at 8:00 AM in your local timezone.</p>
                    <p>Stay safe and prepared! ☔☀️</p>
                </div>
            </body>
            </html>
            """
        else:
            # Regular weather alert template
            html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #f0f8ff; padding: 15px; border-radius: 5px; }}
                    .alert {{ background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                    .weather-info {{ background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                    .footer {{ color: #666; font-size: 12px; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>🌤️ Weather Alert</h2>
                    <p><strong>Location:</strong> {weather_analysis['location']}</p>
                    <p><strong>Time:</strong> {current_time}</p>
                </div>
                
                <div class="weather-info">
                    <h3>Weather Conditions:</h3>
                    <p><strong>Current Temperature:</strong> {weather_analysis['current_temperature']:.1f}°F</p>
                    <p><strong>Daily High:</strong> {weather_analysis['daily_high']:.1f}°F</p>
                    <p><strong>Condition:</strong> {weather_analysis['description'].title()}</p>
                </div>
                
                <div class="alert">
                    <h3>⚠️ Important Reminders:</h3>
                    <ul>
            """
            
            for notification in weather_analysis['notifications']:
                html_body += f"<li>{notification}</li>"
            
            html_body += f"""
                    </ul>
                </div>
                
                <div class="footer">
                    <p>This notification was sent by your Weather Alert System</p>
                    <p>Stay safe and prepared! ☔☀️</p>
                </div>
            </body>
            </html>
            """
        
        return html_body
    
    def send_test_email(self):
        """Send a test email to verify configuration"""
        test_analysis = {
            'location': 'Test Location',
            'temperature': 75.0,
            'description': 'test weather',
            'notifications': ['🧪 This is a test notification to verify your email setup!']
        }
        
        return self.send_email_notification(test_analysis) 
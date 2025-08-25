# 🌤️ Weather Notification System

A Python application that checks weather conditions and sends you email notifications when you need to bring an umbrella or sunscreen!

## Features

- 🌧️ **Rain Detection**: Alerts you when rain is expected
- ☀️ **High Temperature Alerts**: Reminds you about sunscreen when temperature > 80°F
- 📧 **Email Notifications**: Beautiful HTML emails with weather information
- ⏰ **Scheduled Checks**: Automatically checks weather every 30 minutes
- 🎯 **Customizable**: Easy to configure location and notification settings

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your API Keys

#### Weather API (OpenWeatherMap)
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key from your dashboard
4. The free tier allows 60 calls/minute - perfect for this app!

#### Email Setup (Gmail)
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. Use this app password (not your regular Gmail password)

### 3. Configure the Application

1. Copy `env_example.txt` to `.env`:
```bash
cp env_example.txt .env
```

2. Edit `.env` with your information:
```env
WEATHER_API_KEY=your_actual_api_key_here
CITY=Your City
COUNTRY_CODE=US
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=your_email@gmail.com
```

### 4. Run the Application

```bash
python main.py
```

## Usage

When you run the application, you'll see a menu:

1. **Run once** - Check weather immediately
2. **Run scheduled** - Check weather every 30 minutes automatically
3. **Send test email** - Test your email configuration
4. **Exit** - Close the application

## How It Works

1. **Weather Check**: Fetches current weather from OpenWeatherMap API
2. **Analysis**: Checks for:
   - Rain conditions (umbrella needed)
   - High temperature > 80°F (sunscreen needed)
3. **Notification**: Sends beautiful HTML email with weather info and reminders

## Example Notifications

- 🌧️ "Bring an umbrella! Rain is expected."
- ☀️ "High temperature expected. Don't forget sunscreen!"
- ☀️🌧️ "High temperature and rain expected. Bring umbrella AND sunscreen!"

## Customization

You can customize the application by editing `config.py`:

- `TEMPERATURE_THRESHOLD`: Change from 80°F to your preferred temperature
- `CHECK_INTERVAL_MINUTES`: Change how often to check weather
- `RAIN_CONDITIONS`: Modify what weather conditions trigger umbrella alerts

## File Structure

```
weather-email/
├── main.py                 # Main application
├── weather_checker.py      # Weather API integration
├── notification_sender.py  # Email notification system
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
└── README.md             # This file
```

## Troubleshooting

### "Weather API key not found"
- Make sure you've created a `.env` file
- Verify your API key is correct
- Check that OpenWeatherMap API is working

### "Email configuration incomplete"
- Ensure all email fields are filled in `.env`
- Use Gmail App Password, not your regular password
- Check that 2-Factor Authentication is enabled

### "Cannot connect to weather API"
- Verify your internet connection
- Check if your API key is valid
- Ensure you haven't exceeded the free tier limits

## API Information

- **OpenWeatherMap API**: Free tier with 60 calls/minute
- **Gmail SMTP**: Free with Gmail account
- **Location**: Uses city name and country code (e.g., "New York, US")

## Future Enhancements

- 📱 SMS notifications via Twilio
- 🌅 Sunrise/sunset notifications
- 📊 Weather history tracking
- 🎨 Custom notification themes
- 📍 GPS-based location detection

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify your API keys and configuration
3. Make sure all dependencies are installed

---

**Happy weather monitoring! ☔☀️** 
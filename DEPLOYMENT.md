# 🚀 Deployment Guide - Weather Notification App

## Deploy to Heroku (Free Tier)

### Prerequisites:
1. **Git** installed on your computer
2. **Heroku CLI** installed
3. **Heroku account** (free at heroku.com)

### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login to Heroku
```bash
heroku login
```

### Step 3: Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit for deployment"
```

### Step 4: Create Heroku App
```bash
heroku create your-weather-app-name
```

### Step 5: Set Environment Variables
```bash
# Set your API keys and email credentials
heroku config:set WEATHER_API_KEY=56d2e99920ceb5470ea88d9105b886dc
heroku config:set EMAIL_ADDRESS=linzhang995@gmail.com
heroku config:set EMAIL_PASSWORD=hkea aies eerb qans
```

### Step 6: Deploy
```bash
git push heroku main
```

### Step 7: Open Your App
```bash
heroku open
```

## 🌐 Your App Will Be Live At:
`https://your-weather-app-name.herokuapp.com`

## 📧 Share With Friends:
- **Main page**: `https://your-weather-app-name.herokuapp.com`
- **Admin panel**: `https://your-weather-app-name.herokuapp.com/admin`

## 🔧 Important Notes:
- **Free tier**: App sleeps after 30 minutes of inactivity
- **Database**: SQLite file will be reset on each deploy (use PostgreSQL for production)
- **Background service**: May not run continuously on free tier

## 🚀 Next Steps:
1. **Custom domain**: Add your own domain name
2. **PostgreSQL**: Upgrade to paid plan for persistent database
3. **Monitoring**: Add logging and analytics
4. **Scaling**: Upgrade for more users

## 🆘 Troubleshooting:
```bash
# View logs
heroku logs --tail

# Restart app
heroku restart

# Check config
heroku config
```

# 🚂 Railway Deployment Guide

## Quick Deploy to Railway (Free!)

### Step 1: Push to GitHub
```bash
# Create a new GitHub repository
# Then push your code:
git remote add origin https://github.com/YOUR_USERNAME/weather-email.git
git push -u origin master
```

### Step 2: Deploy to Railway
1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **Click "New Project"**
4. **Choose "Deploy from GitHub repo"**
5. **Select your weather-email repository**
6. **Click "Deploy"**

### Step 3: Set Environment Variables
In Railway dashboard:
1. **Go to your project**
2. **Click "Variables" tab**
3. **Add these variables:**
   ```
   WEATHER_API_KEY=56d2e99920ceb5470ea88d9105b886dc
   EMAIL_ADDRESS=linzhang995@gmail.com
   EMAIL_PASSWORD=hkea aies eerb qans
   ```

### Step 4: Get Your URL
- Railway will give you a URL like: `https://your-app-name.railway.app`
- **Share this URL** with friends!

## 🎉 Done!
Your weather app is now live on the internet!

## 📝 Add to README.md:
```markdown
## 🌐 Live Demo
Try the app: https://your-app-name.railway.app

## 🚀 Quick Start
1. Clone this repo
2. Install dependencies: `pip install -r requirements.txt`
3. Set up `.env` file with your API keys
4. Run: `python app.py`
5. Visit: http://localhost:5001
```

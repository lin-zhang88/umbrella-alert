#!/usr/bin/env python3
"""
Test script to verify daily weather check schedule
"""

from datetime import datetime
import time

def test_daily_schedule():
    """Test the daily 8:00 AM schedule logic"""
    print("🧪 Testing Daily Schedule Logic")
    print("=" * 40)
    
    # Test current time
    now = datetime.now()
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 8:00 AM condition
    is_8am = now.hour == 8 and now.minute == 0
    print(f"Is it 8:00 AM? {'✅ Yes' if is_8am else '❌ No'}")
    
    # Show next 8:00 AM
    if now.hour < 8:
        next_8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        # Tomorrow at 8:00 AM
        from datetime import timedelta
        next_8am = (now + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
    
    time_until_8am = next_8am - now
    hours = int(time_until_8am.total_seconds() // 3600)
    minutes = int((time_until_8am.total_seconds() % 3600) // 60)
    
    print(f"Next 8:00 AM: {next_8am.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Time until next check: {hours} hours, {minutes} minutes")
    
    print("\n📋 Schedule Summary:")
    print("• Daily weather checks at 8:00 AM")
    print("• Only sends emails when alerts are needed")
    print("• Welcome email sent to new subscribers")
    print("• Background service runs continuously")

if __name__ == "__main__":
    test_daily_schedule()

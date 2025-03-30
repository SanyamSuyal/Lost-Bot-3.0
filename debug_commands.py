import discord
from discord.ext import commands
import logging
import asyncio
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("command_debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("command_debug")

# Load token from environment
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create test bot with same prefix
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='s!', intents=intents)

# Track command registration
@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")
    
    # Print registered commands
    all_commands = list(bot.commands)
    logger.info(f"Registered {len(all_commands)} commands:")
    for cmd in all_commands:
        logger.info(f"- {cmd.name}")
    
    # Log guilds the bot is in
    guilds = bot.guilds
    logger.info(f"Bot is in {len(guilds)} guilds:")
    for guild in guilds:
        logger.info(f"- {guild.name} (ID: {guild.id})")
        
    # Sync commands
    try:
        logger.info("Syncing commands...")
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} commands")
    except Exception as e:
        logger.error(f"Error syncing commands: {e}")

# Basic test commands
@bot.command(name="test")
async def test(ctx):
    """Test command to verify command processing"""
    logger.info(f"Test command executed by {ctx.author}")
    await ctx.send("Test command received!")

@bot.command(name="debug")
async def debug(ctx):
    """Debug command to show command information"""
    logger.info(f"Debug command executed by {ctx.author}")
    
    # Get all commands
    all_commands = list(bot.commands)
    
    # Create embed
    embed = discord.Embed(
        title="Bot Debug Information",
        description=f"Command prefix: `s!`\nRegistered commands: {len(all_commands)}",
        color=0x5865F2
    )
    
    # Add command list
    cmd_list = "\n".join([f"• `{cmd.name}`" for cmd in all_commands[:15]])
    embed.add_field(name="Commands", value=cmd_list or "No commands registered", inline=False)
    
    # Add bot info
    embed.add_field(
        name="Bot Information",
        value=f"Name: {bot.user.name}\nID: {bot.user.id}\nLatency: {round(bot.latency * 1000)}ms",
        inline=False
    )
    
    # Add guild info
    guilds = bot.guilds
    guild_info = "\n".join([f"• {guild.name} ({guild.member_count} members)" for guild in guilds[:5]])
    embed.add_field(name="Guilds", value=guild_info or "Not in any guilds", inline=False)
    
    await ctx.send(embed=embed)

# Monitor message events
@bot.event
async def on_message(message):
    # Don't process messages from the bot itself
    if message.author.bot:
        return
    
    # Log messages with the command prefix
    if message.content.startswith('s!'):
        logger.info(f"Potential command detected: {message.content}")
        command_name = message.content.split()[0][2:] if ' ' in message.content else message.content[2:]
        cmd = bot.get_command(command_name)
        if cmd:
            logger.info(f"Found matching command: {cmd.name}")
        else:
            logger.warning(f"No matching command found for: {command_name}")
    
    # Continue processing commands
    await bot.process_commands(message)

@bot.event
async def on_command(ctx):
    logger.info(f"Command '{ctx.command.name}' invoked by {ctx.author}")

@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Command error in {ctx.command.name if ctx.command else 'unknown'}: {error}")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Command not found. Try `s!help` to see available commands.")
    else:
        await ctx.send(f"Error executing command: {error}")

# Run the bot
async def main():
    logger.info("Starting debug bot...")
    try:
        await bot.start(TOKEN)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 
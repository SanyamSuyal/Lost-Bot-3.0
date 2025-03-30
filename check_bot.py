import os
import sys
import logging
import discord
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_check.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("bot_check")

def main():
    """Check the bot's configuration and command registration"""
    logger.info("Starting bot check...")
    
    # Check environment variables
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("❌ Discord token not found in environment variables!")
        return
    
    logger.info("✅ Discord token found")
    
    # Check intents configuration
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    logger.info("Intents configuration:")
    logger.info(f"- message_content: {intents.message_content}")
    logger.info(f"- members: {intents.members}")
    logger.info(f"- guilds: {intents.guilds}")
    
    # Check Python version
    logger.info(f"Python version: {sys.version}")
    
    # Check discord.py version
    logger.info(f"discord.py version: {discord.__version__}")
    
    # Check cogs directory
    cogs_dir = './cogs'
    if not os.path.exists(cogs_dir):
        logger.error(f"❌ Cogs directory not found: {cogs_dir}")
        possible_locations = ['./cogs', '/opt/render/project/src/cogs', '../cogs', '../../cogs']
        for loc in possible_locations:
            if os.path.exists(loc):
                logger.info(f"✅ Found alternate cogs directory: {loc}")
                cogs_dir = loc
                break
    else:
        logger.info(f"✅ Cogs directory found: {cogs_dir}")
    
    # Check cog files
    cog_files = []
    if os.path.exists(cogs_dir):
        cog_files = [f for f in os.listdir(cogs_dir) if f.endswith('.py')]
        logger.info(f"Found {len(cog_files)} cog files: {cog_files}")
        
        # Check for common command definitions in cogs
        for cog_file in cog_files:
            cog_path = os.path.join(cogs_dir, cog_file)
            try:
                with open(cog_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    cmd_count = content.count('@commands.command')
                    logger.info(f"File {cog_file} has {cmd_count} commands defined")
                    
                    # Check for command prefix usage
                    if 's!' in content:
                        logger.info(f"✅ Command prefix 's!' found in {cog_file}")
                    else:
                        logger.warning(f"⚠️ Command prefix 's!' not found in {cog_file}")
            except Exception as e:
                logger.error(f"❌ Error checking cog file {cog_file}: {e}")
    else:
        logger.error("❌ Could not find any cogs directory to check files!")
    
    # Check command registration in main.py
    if os.path.exists('main.py'):
        logger.info("Checking main.py for command configuration")
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'command_prefix=\'s!\'' in content:
                logger.info("✅ Command prefix 's!' configured in main.py")
            else:
                logger.warning("⚠️ Command prefix 's!' not found in main.py")
            
            if 'intents.message_content = True' in content:
                logger.info("✅ message_content intent enabled in main.py")
            else:
                logger.warning("⚠️ message_content intent may not be enabled in main.py")
    
    logger.info("Bot check completed")

if __name__ == "__main__":
    main() 
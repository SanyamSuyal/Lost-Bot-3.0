import os
import shutil
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("setup.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("setup")

def main():
    """Set up the environment for the bot to run properly"""
    logger.info("Starting environment check...")
    
    # Check current directory and print contents
    current_dir = os.getcwd()
    logger.info(f"Current directory: {current_dir}")
    
    try:
        dir_contents = os.listdir(current_dir)
        logger.info(f"Directory contents: {dir_contents}")
    except Exception as e:
        logger.error(f"Error listing directory: {e}")
    
    # Check if we're in a Render environment
    is_render = os.environ.get('RENDER') == 'true'
    logger.info(f"Running in Render environment: {is_render}")
    
    # Ensure cogs directory exists
    cogs_dir = os.path.join(current_dir, 'cogs')
    if not os.path.exists(cogs_dir):
        logger.info("Creating cogs directory...")
        os.makedirs(cogs_dir, exist_ok=True)
    
    # Ensure data directory exists
    data_dir = os.path.join(current_dir, 'data')
    if not os.path.exists(data_dir):
        logger.info("Creating data directory...")
        os.makedirs(data_dir, exist_ok=True)
    
    # Check if any Python files exist in the cogs directory
    cogs_files = [f for f in os.listdir(cogs_dir) if f.endswith('.py')] if os.path.exists(cogs_dir) else []
    logger.info(f"Cogs directory contains {len(cogs_files)} Python files: {cogs_files}")
    
    # If in Render and no cog files, try to copy from src directory
    if is_render and len(cogs_files) == 0:
        src_cogs_dir = '/opt/render/project/src/cogs'
        if os.path.exists(src_cogs_dir):
            logger.info(f"Found cogs in {src_cogs_dir}, copying...")
            for filename in os.listdir(src_cogs_dir):
                if filename.endswith('.py'):
                    src_file = os.path.join(src_cogs_dir, filename)
                    dst_file = os.path.join(cogs_dir, filename)
                    try:
                        shutil.copy2(src_file, dst_file)
                        logger.info(f"Copied {src_file} to {dst_file}")
                    except Exception as e:
                        logger.error(f"Error copying {src_file}: {e}")
    
    # Check Python path
    logger.info(f"Python path: {sys.path}")
    
    # Add current directory to path if not already there
    if current_dir not in sys.path:
        logger.info(f"Adding {current_dir} to Python path")
        sys.path.insert(0, current_dir)
    
    # Log Python modules
    logger.info(f"Python version: {sys.version}")
    
    logger.info("Environment check completed")
    return True

if __name__ == "__main__":
    main() 
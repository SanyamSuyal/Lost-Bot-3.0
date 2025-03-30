import os
import shutil
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("render_setup.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("render_setup")

def main():
    """Set up the Render environment for the bot"""
    logger.info("Starting Render environment setup...")
    
    # Check current directory
    current_dir = os.getcwd()
    logger.info(f"Current directory: {current_dir}")
    
    # Get the Render base directory if we're in a Render environment
    render_dir = os.environ.get('RENDER_PROJECT_DIR', '/opt/render/project')
    src_dir = os.path.join(render_dir, 'src')
    logger.info(f"Render source directory: {src_dir}")
    
    # Define the source and destination directories
    source_cogs_dir = os.path.join(current_dir, 'cogs')
    dest_cogs_dir = os.path.join(src_dir, 'cogs')
    
    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_cogs_dir):
        os.makedirs(dest_cogs_dir, exist_ok=True)
        logger.info(f"Created destination directory: {dest_cogs_dir}")
    
    # Check if source directory exists
    if not os.path.exists(source_cogs_dir):
        logger.error(f"Source directory not found: {source_cogs_dir}")
        return False
    
    # List files in source directory
    cogs_files = [f for f in os.listdir(source_cogs_dir) if f.endswith('.py')]
    logger.info(f"Found {len(cogs_files)} cog files to copy")
    
    # Copy each file
    for filename in cogs_files:
        source_file = os.path.join(source_cogs_dir, filename)
        dest_file = os.path.join(dest_cogs_dir, filename)
        try:
            shutil.copy2(source_file, dest_file)
            logger.info(f"Copied {source_file} to {dest_file}")
        except Exception as e:
            logger.error(f"Error copying {source_file}: {e}")
    
    # Verify the files were copied
    copied_files = [f for f in os.listdir(dest_cogs_dir) if f.endswith('.py')]
    logger.info(f"Destination directory now contains {len(copied_files)} Python files: {copied_files}")
    
    # Check if the Python modules can be imported
    sys.path.insert(0, src_dir)
    try:
        import importlib
        for filename in copied_files:
            module_name = f"cogs.{filename[:-3]}"
            try:
                importlib.import_module(module_name)
                logger.info(f"Successfully imported {module_name}")
            except Exception as e:
                logger.error(f"Error importing {module_name}: {e}")
    except Exception as e:
        logger.error(f"Error testing imports: {e}")
    
    logger.info("Render environment setup completed")
    return True

if __name__ == "__main__":
    main() 
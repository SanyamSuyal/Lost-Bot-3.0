import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("token_check.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("token_check")

def main():
    """Check if the token is properly set in environment variables"""
    logger.info("Checking token...")
    
    # First try loading from .env file
    load_dotenv()
    
    # Get token from environment
    token = os.getenv('DISCORD_TOKEN')
    admin_role = os.getenv('ADMIN_ROLE_ID')
    ltc_address = os.getenv('LTC_ADDRESS')
    
    # Check if token exists and is valid
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        env_vars = [k for k in os.environ.keys()]
        logger.info(f"Available environment variables: {env_vars}")
        
        # Try to create a temporary .env file for testing
        logger.info("Creating a temporary .env file for debugging...")
        with open('.env.debug', 'w') as f:
            f.write(f"# Debug .env file\n")
            f.write(f"DISCORD_TOKEN=YOUR_TOKEN_HERE\n")
            f.write(f"ADMIN_ROLE_ID=YOUR_ADMIN_ROLE_ID\n")
            f.write(f"LTC_ADDRESS=YOUR_LTC_ADDRESS\n")
        
        logger.info("Please add your token to the .env file or set it in Render's environment variables")
        return False
    else:
        # Validate token format (Discord tokens are generally 59+ characters)
        if len(token) < 50:
            logger.error(f"Token seems invalid (too short, length={len(token)})")
            return False
        
        logger.info(f"Token found! Length: {len(token)}, first 5 chars: {token[:5]}...")
    
    # Check admin role ID
    if not admin_role:
        logger.warning("ADMIN_ROLE_ID not found in environment variables!")
    else:
        logger.info(f"Admin role ID found: {admin_role}")
    
    # Check LTC address
    if not ltc_address:
        logger.warning("LTC_ADDRESS not found in environment variables!")
    else:
        logger.info(f"LTC address found: {ltc_address}")
    
    # Check if we're in Render
    if os.environ.get('RENDER') == 'true':
        logger.info("Running in Render environment")
        
        # Print some Render-specific environment variables
        render_vars = {k: v for k, v in os.environ.items() if k.startswith('RENDER_')}
        logger.info(f"Render environment variables: {list(render_vars.keys())}")
    else:
        logger.info("Not running in Render environment")
    
    logger.info("Token check completed")
    return True

if __name__ == "__main__":
    main() 
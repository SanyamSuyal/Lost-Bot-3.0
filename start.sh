#!/bin/bash
# Start script for Render

# Debug: Print current directory
echo "Current directory: $(pwd)"
echo "Listing directory contents:"
ls -la

# Make sure required directories exist
mkdir -p ./data
mkdir -p ./cogs

# Debug: Check if cogs directory now exists
echo "After mkdir, checking cogs directory:"
ls -la ./cogs || echo "Failed to list cogs directory"

# If cogs directory is empty, try to copy from src directory
if [ -d "/opt/render/project/src/cogs" ] && [ ! "$(ls -A ./cogs)" ]; then
  echo "Cogs directory is empty, copying from src directory..."
  cp -r /opt/render/project/src/cogs/* ./cogs/
  echo "After copying, cogs directory contains:"
  ls -la ./cogs
fi

# Check if .env file exists and create a debug version if not
if [ ! -f ".env" ]; then
  echo "No .env file found, creating a placeholder for debugging..."
  echo "# Placeholder .env file - replace with real values" > .env
  echo "# These are retrieved from Render environment variables" >> .env
  echo "DISCORD_TOKEN=from_render_env" >> .env
  echo "ADMIN_ROLE_ID=from_render_env" >> .env
  echo "LTC_ADDRESS=from_render_env" >> .env
fi

# Check environment variables
echo "Environment variables check:"
echo "DISCORD_TOKEN exists: $(if [ -n \"$DISCORD_TOKEN\" ]; then echo YES; else echo NO; fi)"
echo "ADMIN_ROLE_ID exists: $(if [ -n \"$ADMIN_ROLE_ID\" ]; then echo YES; else echo NO; fi)"
echo "LTC_ADDRESS exists: $(if [ -n \"$LTC_ADDRESS\" ]; then echo YES; else echo NO; fi)"

# Set debug environment variables
export DISCORD_DEBUG=1
export DISCORD_COMMAND_DEBUG=1

# Run token check script
echo "Running token check script..."
python restart_check.py

# Run environment check script
echo "Running environment check script..."
python check_environment.py

# Run the bot with proper error output and debug flags
echo "Starting bot..."
python main.py 2>&1 | tee bot_error.log 
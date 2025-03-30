# Discord Shop Bot

A powerful Discord bot for managing an online shop with cryptocurrency (LTC) payments.

## Features

### User Commands
- `s!shop` – View all available items with prices, stock, and descriptions
- `s!buy <item>` – Purchase an item and receive payment instructions
- `s!price <item>` – Check the current price of an item
- `s!stock <item>` – Check available stock for an item
- `s!orders` – View past and pending orders
- `s!cancelorder <order_id>` – Cancel an order before payment
- `s!refund <order_id>` – Request a refund if eligible
- `s!help` – Get a list of commands and bot functions

### Admin Commands
- `s!additem <name> <price> <stock> <description>` – Add a new product to the store
- `s!removeitem <name>` – Remove an existing product
- `s!setprice <name> <new_price>` – Update the price of an item
- `s!setstock <name> <new_stock>` – Update the stock of an item
- `s!editdescription <name> <new_description>` – Update product descriptions
- `s!restock <name> <amount>` – Increase stock for a specific item
- `s!vieworders [status]` – List all orders (paid, pending, completed)
- `s!orderinfo <order_id>` – View details of a specific order
- `s!deliver <order_id> [delivery_message]` – Mark an order as delivered and send the product
- `s!salesreport [day|week|month]` – Generate a sales report
- `s!resetshop` – WARNING: Wipes all items from the shop
- `s!ban <user> [reason]` – Blacklist a user from purchasing
- `s!unban <user>` – Remove a user from the blacklist
- `s!listbans` – View all blacklisted users
- `s!updatepayment <order_id>` – Manually mark an order as paid

## Setup and Installation

### Requirements
- Python 3.8 or higher
- discord.py
- aiosqlite
- python-dotenv

### Installation Steps

1. Clone this repository
```
git clone https://github.com/yourusername/discord-shop-bot.git
cd discord-shop-bot
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Create a `.env` file based on the `.env.example` template
```
cp .env.example .env
```

4. Edit the `.env` file with your Discord bot token and LTC address

5. Run the bot
```
python main.py
```

## Cryptocurrency Payment Integration

The bot uses a simplified payment system with a single LTC address. When a user purchases an item:

1. The bot creates an order record in the database
2. The user receives payment instructions with the LTC address
3. After payment, an admin can verify the transaction and mark the order as paid
4. The admin can then deliver the product to the customer

## Database
The bot uses SQLite for data storage. The database file is created automatically on first run.

## Support

For questions or issues, please open a GitHub issue or contact the maintainer directly.

# Discord Shop Bot - Render Deployment Guide

This guide will walk you through setting up your Discord Shop Bot on Render.com.

## Prerequisites

1. A [Render.com](https://render.com) account
2. Your Discord bot token (from [Discord Developer Portal](https://discord.com/developers/applications))
3. Your Litecoin address for payments
4. The Discord admin role ID from your server

## Deployment Steps

### 1. Prepare Your Repository

If using GitHub:
- Push your bot code to a GitHub repository
- Make sure you have the following files:
  - `requirements.txt` (dependencies)
  - `start.sh` (start script for Render)
  - All your bot files

### 2. Create a New Web Service on Render

1. Log in to your Render dashboard
2. Click "New+" in the top right and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: Choose a name (e.g., "discord-shop-bot")
   - **Environment**: Select "Python 3"
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash start.sh`
   - **Plan**: Select "Free" for testing, or choose a paid plan for production

### 3. Set Environment Variables

In the Render dashboard for your web service, go to "Environment" tab and add:

- `DISCORD_TOKEN`: Your Discord bot token
- `LTC_ADDRESS`: Your Litecoin address
- `ADMIN_ROLE_ID`: Your admin role ID from Discord

### 4. Deploy

1. Click "Create Web Service"
2. Wait for the deployment to complete
3. Your bot should come online automatically

### Troubleshooting

If your bot doesn't come online:

1. Check the Render logs for errors
2. Verify all environment variables are set correctly
3. Make sure your bot token is valid and has the correct permissions

### Notes

- The free plan will spin down after inactivity. Consider a paid plan for continuous operation.
- SQLite database is stored in the application's directory. For data persistence across deployments, consider using Render's disk service.

## Upgrading

To update your bot:
1. Push changes to your GitHub repository
2. Render will automatically deploy the updates

## Database Backup

For backing up your SQLite database:
1. Go to the Render dashboard
2. Click on "Shell" to access a terminal
3. Run `cp shop_database.db shop_database.backup.db`
4. Use `curl` to download the backup file 
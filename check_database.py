import sqlite3
import os

print("Starting database check...")

# Connect to the database
try:
    conn = sqlite3.connect('shop_database.db')
    print("Connected to database")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check if the database exists and has tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Found tables: {[table['name'] for table in tables]}")

    # Check if items table exists and has the expected structure
    try:
        cursor.execute("PRAGMA table_info(items)")
        columns = cursor.fetchall()
        print(f"Items table columns: {[col['name'] for col in columns]}")
    except sqlite3.Error as e:
        print(f"Error checking items table structure: {e}")

    # Check items table for drive links
    print("\n==== ITEMS TABLE ====")
    try:
        cursor.execute("SELECT id, name, drive_link FROM items")
        items = cursor.fetchall()

        if items:
            print(f"Found {len(items)} products:")
            for item in items:
                drive_link = item['drive_link'] if item['drive_link'] else "NO LINK FOUND"
                print(f"ID: {item['id']} | Name: {item['name']} | Drive Link: {drive_link}")
        else:
            print("No items found in the database.")
    except sqlite3.Error as e:
        print(f"Error querying items: {e}")

    # Check orders table
    print("\n==== ORDERS TABLE ====")
    try:
        cursor.execute("""
            SELECT o.id, o.status, o.payment_confirmed, i.name 
            FROM orders o
            JOIN items i ON o.item_id = i.id
            ORDER BY o.id DESC
            LIMIT 5
        """)
        orders = cursor.fetchall()

        if orders:
            print(f"Last {len(orders)} orders:")
            for order in orders:
                confirmed = "Yes" if order['payment_confirmed'] == 1 else "No"
                print(f"Order ID: {order['id']} | Item: {order['name']} | Status: {order['status']} | Confirmed: {confirmed}")
        else:
            print("No orders found in the database.")
            
        # Try to get drive links for items in orders
        cursor.execute("""
            SELECT o.id, i.id as item_id, i.name, i.drive_link
            FROM orders o
            JOIN items i ON o.item_id = i.id
            ORDER BY o.id DESC
            LIMIT 5
        """)
        order_items = cursor.fetchall()
        
        if order_items:
            print("\n==== DRIVE LINKS FOR RECENT ORDERS ====")
            for item in order_items:
                drive_link = item['drive_link'] if item['drive_link'] else "NO LINK FOUND"
                print(f"Order ID: {item['id']} | Item ID: {item['item_id']} | Name: {item['name']} | Drive Link: {drive_link}")
        
    except sqlite3.Error as e:
        print(f"Error querying orders: {e}")

    # Close the connection
    conn.close()
    print("\nDatabase connection closed")

except Exception as e:
    print(f"Error: {e}")

print("\nTo auto-deliver an item, use this command:")
print("s!approve <order_id> AUTODELIVER Your message here") 
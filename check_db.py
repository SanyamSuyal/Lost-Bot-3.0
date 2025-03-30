import sqlite3

# Connect to the database
conn = sqlite3.connect('shop_database.db')
cursor = conn.cursor()

# Check items
print("\n==== ITEMS TABLE ====")
cursor.execute("SELECT id, name, drive_link FROM items")
items = cursor.fetchall()
for item in items:
    print(f"ID: {item[0]} | Name: {item[1]} | Drive Link: {item[2] if item[2] else 'NONE'}")

# Close connection
conn.close() 
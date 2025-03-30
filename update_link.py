import sqlite3

# Connect to the database
conn = sqlite3.connect('shop_database.db')
cursor = conn.cursor()

# Update the drive link for the Music_Bot product (ID 1)
new_drive_link = "https://youtube.com/shorts/JNjPOfeKKfQ?si=p7JjysCjbfYWCGIK"  # Replace with your actual drive link
cursor.execute("UPDATE items SET drive_link = ? WHERE id = 1", (new_drive_link,))
conn.commit()

# Verify the update
cursor.execute("SELECT id, name, drive_link FROM items WHERE id = 1")
item = cursor.fetchone()
if item:
    print(f"Updated drive link for {item[1]}:")
    print(f"ID: {item[0]} | Name: {item[1]} | Drive Link: {item[2]}")
else:
    print("Product with ID 1 not found.")

# Close the connection
conn.close()

print("\nNow use this command to auto-deliver:")
print("s!approve <order_id> AUTODELIVER Your message here") 
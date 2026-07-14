from database.database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("DELETE FROM users")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")

conn.commit()
conn.close()

print("✅ Users table has been cleared successfully.")
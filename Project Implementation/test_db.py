from database.database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
SELECT id, full_name, username, email, role
FROM users
""")

rows = cursor.fetchall()

for row in rows:
    print(dict(row))

conn.close()
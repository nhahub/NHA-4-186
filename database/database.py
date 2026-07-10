import sqlite3
from pathlib import Path

# ======================================================
# Database Path
# ======================================================

DB_PATH = Path(__file__).parent / "maintenance.db"


# ======================================================
# Create Connection
# ======================================================

def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    conn = sqlite3.connect(DB_PATH)

    # Access columns by name
    conn.row_factory = sqlite3.Row

    # Enable Foreign Keys
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# ======================================================
# Close Connection
# ======================================================

def close_connection(conn):
    """
    Safely close the database connection.
    """

    if conn:
        conn.close()


# ======================================================
# Test Connection
# ======================================================

if __name__ == "__main__":

    try:
        conn = get_connection()

        print("✅ Database connected successfully.")

        close_connection(conn)

    except Exception as e:

        print(f"❌ Database connection failed: {e}")
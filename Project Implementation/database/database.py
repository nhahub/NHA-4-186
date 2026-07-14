import sqlite3
from pathlib import Path

# ======================================================
# Database Path
# ======================================================

DB_PATH = Path(__file__).parent / "maintenance.db"


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


# ======================================================
# Create Connection
# ======================================================

def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    conn = sqlite3.connect(DB_PATH)

    # Access columns by name
    conn.row_factory = dict_factory

    # Enable Foreign Keys
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def get_pandas_connection():
    """
    Create a connection for pd.read_sql_query (no dict_factory).
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
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
import sqlite3
from database.database import get_connection


def create_tables():
    """
    Create all database tables if they don't already exist.
    """

    conn = get_connection()
    cursor = conn.cursor()
# ======================================================
# Users Table
# ======================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT NOT NULL,

        username TEXT UNIQUE NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT NOT NULL CHECK(role IN ('Admin','Engineer')),

        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    # ======================================================
    # Predictions Table
    # ======================================================

    cursor.execute("""
   CREATE TABLE IF NOT EXISTS predictions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    engine_id INTEGER,

    user_id INTEGER NOT NULL,

    prediction_date TEXT NOT NULL,

    predicted_rul REAL NOT NULL,

    health_status TEXT NOT NULL,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);
""")

    # ======================================================
    # Sensor Readings Table
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            prediction_id INTEGER NOT NULL,

            op_setting_1 REAL,
            op_setting_2 REAL,

            sensor_2 REAL,
            sensor_3 REAL,
            sensor_4 REAL,
            sensor_6 REAL,
            sensor_7 REAL,
            sensor_8 REAL,
            sensor_9 REAL,
            sensor_11 REAL,
            sensor_12 REAL,
            sensor_13 REAL,
            sensor_14 REAL,
            sensor_15 REAL,
            sensor_17 REAL,
            sensor_20 REAL,
            sensor_21 REAL,

            FOREIGN KEY (prediction_id)
            REFERENCES predictions(id)
            ON DELETE CASCADE
        );
    """)

    # ======================================================
# Maintenance Table
# ======================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS maintenance (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        engine_id INTEGER NOT NULL,

        user_id INTEGER NOT NULL,

        maintenance_date TEXT NOT NULL,

        maintenance_type TEXT NOT NULL,

        notes TEXT,

        status TEXT NOT NULL DEFAULT 'Completed',

        cost REAL DEFAULT 0,

        downtime_hours REAL DEFAULT 0,

        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
    );
""")

    try:
        cursor.execute("ALTER TABLE maintenance ADD COLUMN status TEXT NOT NULL DEFAULT 'Completed'")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE maintenance ADD COLUMN cost REAL DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE maintenance ADD COLUMN downtime_hours REAL DEFAULT 0")
    except sqlite3.OperationalError:
        pass

create_tables()

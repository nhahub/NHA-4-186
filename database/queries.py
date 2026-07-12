import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from database.database import get_connection, get_pandas_connection


# ======================================================
# Users
# ======================================================

def create_user(full_name, username, email, password, role):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (full_name, username, email, password, role)
            VALUES (?, ?, ?, ?, ?)
        """, (full_name, username, email, password, role))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ======================================================

def get_user_by_username(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    return user


# ======================================================

def get_all_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        ORDER BY full_name
    """)

    users = cursor.fetchall()

    conn.close()

    return users


# ======================================================

def update_user(user_id, full_name, email, role):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET
            full_name=?,
            email=?,
            role=?
        WHERE id=?
    """, (full_name, email, role, user_id))

    conn.commit()
    conn.close()


# ======================================================

def get_critical_engines_without_maintenance():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT engine_id, predicted_rul, prediction_date
        FROM (
            SELECT engine_id, predicted_rul, health_status, prediction_date,
                   ROW_NUMBER() OVER (PARTITION BY engine_id ORDER BY prediction_date DESC) AS rn
            FROM predictions
        ) latest
        WHERE rn = 1 AND health_status = 'Critical'
        AND NOT EXISTS (
            SELECT 1 FROM maintenance m
            WHERE m.engine_id = latest.engine_id
            AND m.maintenance_date >= latest.prediction_date
        )
        ORDER BY predicted_rul ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_maintenance_kpis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS cnt FROM maintenance
        WHERE status = 'Pending'
    """)
    pending_count = cursor.fetchone()["cnt"]

    seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
    cursor.execute("""
        SELECT COUNT(*) AS cnt FROM maintenance
        WHERE status = 'Pending' AND maintenance_date < ?
    """, (seven_days_ago,))
    overdue = cursor.fetchone()["cnt"]

    this_month = datetime.now().strftime("%Y-%m")
    cursor.execute("""
        SELECT COUNT(*) AS cnt FROM maintenance
        WHERE maintenance_date LIKE ?
    """, (f"{this_month}%",))
    monthly = cursor.fetchone()["cnt"]

    cursor.execute("""
        SELECT maintenance_date FROM maintenance
        ORDER BY maintenance_date DESC LIMIT 1
    """)
    last = cursor.fetchone()
    avg_days = 0
    if last:
        last_date = datetime.fromisoformat(last["maintenance_date"])
        avg_days = (datetime.now() - last_date).days

    conn.close()
    return {
        "overdue_count": int(overdue),
        "avg_days_since_last_maintenance": avg_days,
        "maintenance_this_month": int(monthly),
        "pending_count": int(pending_count)
    }


def update_maintenance_status(maintenance_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE maintenance SET status = ? WHERE id = ?", (status, maintenance_id))
    conn.commit()
    conn.close()


def get_maintenance_and_predictions_by_engine(engine_id):
    conn = get_pandas_connection()
    df_pred = pd.read_sql_query("""
        SELECT prediction_date, predicted_rul, health_status
        FROM predictions
        WHERE engine_id = ?
        ORDER BY prediction_date ASC
    """, conn, params=(engine_id,))
    df_maint = pd.read_sql_query("""
        SELECT maintenance_date, maintenance_type, notes
        FROM maintenance
        WHERE engine_id = ?
        ORDER BY maintenance_date ASC
    """, conn, params=(engine_id,))
    conn.close()
    return df_pred, df_maint


def delete_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE id=?
    """, (user_id,))

    conn.commit()
    conn.close()


def insert_maintenance(engine_id, user_id, maintenance_type, notes, status="Completed", cost=0, downtime_hours=0, maintenance_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    mdate = maintenance_date or datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO maintenance (engine_id, user_id, maintenance_date, maintenance_type, notes, status, cost, downtime_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (engine_id, user_id, mdate, maintenance_type, notes, status, cost, downtime_hours))
    conn.commit()
    conn.close()


def get_all_maintenance():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.engine_id, m.maintenance_date, m.maintenance_type, m.notes,
               m.status, m.cost, m.downtime_hours, u.full_name
        FROM maintenance m
        LEFT JOIN users u ON m.user_id = u.id
        ORDER BY m.maintenance_date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def insert_prediction(user_id, engine_id, predicted_rul, health_status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            engine_id,
            user_id,
            prediction_date,
            predicted_rul,
            health_status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        engine_id,
        user_id,
        datetime.now().isoformat(),
        predicted_rul,
        health_status
    ))

    conn.commit()

    prediction_id = cursor.lastrowid

    conn.close()

    return prediction_id
def insert_sensor_readings(prediction_id, sensor_data: dict):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sensor_readings (
            prediction_id,
            op_setting_1,
            op_setting_2,
            sensor_2,
            sensor_3,
            sensor_4,
            sensor_6,
            sensor_7,
            sensor_8,
            sensor_9,
            sensor_11,
            sensor_12,
            sensor_13,
            sensor_14,
            sensor_15,
            sensor_17,
            sensor_20,
            sensor_21
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        prediction_id,
        sensor_data.get("op_setting_1"),
        sensor_data.get("op_setting_2"),
        sensor_data.get("sensor_2"),
        sensor_data.get("sensor_3"),
        sensor_data.get("sensor_4"),
        sensor_data.get("sensor_6"),
        sensor_data.get("sensor_7"),
        sensor_data.get("sensor_8"),
        sensor_data.get("sensor_9"),
        sensor_data.get("sensor_11"),
        sensor_data.get("sensor_12"),
        sensor_data.get("sensor_13"),
        sensor_data.get("sensor_14"),
        sensor_data.get("sensor_15"),
        sensor_data.get("sensor_17"),
        sensor_data.get("sensor_20"),
        sensor_data.get("sensor_21")
    ))

    conn.commit()
    conn.close()
    
def get_predictions_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        WHERE user_id = ?
        ORDER BY prediction_date DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_latest_prediction_per_engine():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.* FROM predictions p
        INNER JOIN (
            SELECT engine_id, MAX(prediction_date) as max_date
            FROM predictions GROUP BY engine_id
        ) latest ON p.engine_id = latest.engine_id AND p.prediction_date = latest.max_date
        ORDER BY p.predicted_rul ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_predictions_by_engine(engine_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM predictions WHERE engine_id = ? ORDER BY prediction_date DESC",
        (engine_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_maintenance_by_engine(engine_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM maintenance WHERE engine_id = ? ORDER BY maintenance_date DESC",
        (engine_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_maintenance_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM maintenance")
    row = cursor.fetchone()
    conn.close()
    return row["cnt"] if row else 0


def get_engines_with_maintenance():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT engine_id) as cnt FROM maintenance")
    row = cursor.fetchone()
    conn.close()
    return row["cnt"] if row else 0


def get_recent_maintenance(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.*, u.full_name as engineer_name
        FROM maintenance m
        LEFT JOIN users u ON m.user_id = u.id
        ORDER BY m.maintenance_date DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_prediction_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM predictions")
    row = cursor.fetchone()
    conn.close()
    return row["cnt"] if row else 0
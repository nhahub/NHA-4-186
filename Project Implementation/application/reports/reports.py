import pandas as pd
from database.database import get_pandas_connection as get_connection


# ======================================================
# 1. Dashboard KPIs
# ======================================================
def get_dashboard_kpis():
    """
    Returns dashboard summary statistics.
    """
    conn = get_connection()

    users = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM users", conn
    ).iloc[0]["total"]

    predictions = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM predictions", conn
    ).iloc[0]["total"]

    maintenance = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM maintenance", conn
    ).iloc[0]["total"]

    critical = pd.read_sql_query("""
        SELECT COUNT(DISTINCT engine_id) AS total
        FROM predictions
        WHERE health_status IN ('High Risk','Critical','Poor')
    """, conn).iloc[0]["total"]

    conn.close()

    return {
        "users": int(users),
        "predictions": int(predictions),
        "maintenance": int(maintenance),
        "critical": int(critical)
    }


# ======================================================
# 2. Prediction Summary
# ======================================================
def get_prediction_summary():
    """
    Returns summary statistics for predictions.
    """
    conn = get_connection()

    query = """
        SELECT
            COUNT(id) AS Total_Predictions,
            ROUND(AVG(predicted_rul), 2) AS Average_RUL,
            MIN(predicted_rul) AS Minimum_RUL,
            MAX(predicted_rul) AS Maximum_RUL
        FROM predictions
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    if not df.empty:
        return df.iloc[0].to_dict()

    return {
        "Total_Predictions": 0,
        "Average_RUL": 0,
        "Minimum_RUL": 0,
        "Maximum_RUL": 0
    }


# ======================================================
# 3. Critical Engines Report
# ======================================================
def get_critical_engines():
    """
    Returns engines that are considered high risk.
    """
    conn = get_connection()

    query = """
        SELECT
            p.engine_id,
            p.predicted_rul,
            p.health_status,
            p.prediction_date,
            u.full_name
        FROM predictions p
        LEFT JOIN users u
        ON p.user_id = u.id
        WHERE
            p.health_status IN ('High Risk','Critical','Poor')
            OR p.predicted_rul < 30
        ORDER BY p.predicted_rul ASC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# ======================================================
# 4. Recent Predictions
# ======================================================
def get_recent_predictions(limit=20):
    """
    Returns the latest AI predictions.
    """
    conn = get_connection()

    query = """
        SELECT
            engine_id,
            predicted_rul,
            health_status,
            prediction_date
        FROM predictions
        ORDER BY prediction_date DESC
        LIMIT ?
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(limit,)
    )

    conn.close()

    return df


# ======================================================
# 5. Maintenance History
# ======================================================
def get_maintenance_history():
    """
    Returns maintenance history.
    """
    conn = get_connection()

    query = """
        SELECT
            m.engine_id,
            m.maintenance_date,
            m.maintenance_type,
            m.notes,
            m.status,
            m.cost,
            m.downtime_hours,
            u.full_name
        FROM maintenance m
        LEFT JOIN users u
        ON m.user_id = u.id
        ORDER BY m.maintenance_date DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# ======================================================
# 6. Maintenance History by Engine
# ======================================================
def get_maintenance_by_engine(engine_id):
    """
    Returns maintenance history for a specific engine.
    """
    conn = get_connection()

    query = """
        SELECT
            maintenance_date,
            maintenance_type,
            notes,
            status,
            cost,
            downtime_hours
        FROM maintenance
        WHERE engine_id = ?
        ORDER BY maintenance_date DESC
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(engine_id,)
    )

    conn.close()

    return df


# ======================================================
# 7. Engineer Activity Report
# ======================================================
def get_engineer_activity():
    """
    Returns engineer activity statistics.
    """
    conn = get_connection()

    query = """
        SELECT
            u.full_name AS Engineer_Name,

            (
                SELECT COUNT(*)
                FROM predictions p
                WHERE p.user_id = u.id
            ) AS Predictions_Count,

            (
                SELECT COUNT(*)
                FROM maintenance m
                WHERE m.user_id = u.id
            ) AS Maintenance_Count

        FROM users u

        WHERE u.role='Engineer'

        ORDER BY
            Predictions_Count DESC,
            Maintenance_Count DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# ======================================================
# 8. Health Status Distribution
# ======================================================
def get_health_status_distribution():
    """
    Returns health status distribution.
    """
    conn = get_connection()

    query = """
        SELECT
            health_status,
            COUNT(*) AS total
        FROM predictions
        GROUP BY health_status
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# ======================================================
# 9. Maintenance Type Distribution
# ======================================================
def get_maintenance_type_distribution():
    """
    Returns maintenance type distribution.
    """
    conn = get_connection()

    query = """
        SELECT
            maintenance_type,
            COUNT(*) AS total
        FROM maintenance
        GROUP BY maintenance_type
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# ======================================================
# 10. Prediction Trend
# ======================================================
def get_prediction_trend():
    """
    Returns prediction count over time.
    """
    conn = get_connection()

    query = """
        SELECT
            DATE(prediction_date) AS day,
            COUNT(*) AS total
        FROM predictions
        GROUP BY DATE(prediction_date)
        ORDER BY day
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# ======================================================
# 11. Export DataFrame to CSV
# ======================================================
def export_dataframe_to_csv(df):
    """
    Converts a DataFrame into CSV bytes.
    """
    return df.to_csv(index=False).encode("utf-8")
# ======================================================
# 12. Search Prediction by Engine
# ======================================================

def get_predictions_by_engine(engine_id):
    """
    Returns prediction history for a specific engine.
    """
    conn = get_connection()

    query = """
        SELECT
            engine_id,
            predicted_rul,
            health_status,
            prediction_date
        FROM predictions
        WHERE engine_id = ?
        ORDER BY prediction_date DESC
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(engine_id,)
    )

    conn.close()

    return df
# ======================================================
# 13. Prediction by Health Status
# ======================================================

def get_predictions_by_status(status):
    """
    Returns predictions filtered by health status.
    """
    conn = get_connection()

    query = """
        SELECT
            engine_id,
            predicted_rul,
            health_status,
            prediction_date
        FROM predictions
        WHERE health_status = ?
        ORDER BY prediction_date DESC
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(status,)
    )

    conn.close()

    return df

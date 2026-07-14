import streamlit as st
import pandas as pd
from utils.path_setup import *
from utils.styles import inject_global_css, status_badge_html
from utils.sidebar import render_sidebar
from database.queries import get_predictions_by_user

st.set_page_config(
    page_title="Prediction History",
    page_icon="📜",
    layout="wide"
)

inject_global_css()
render_sidebar()

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login first")
    st.stop()

st.markdown(
    '<div class="main-header"><h1>📜 Prediction History</h1><p>View and analyze your past predictions</p></div>',
    unsafe_allow_html=True,
)

user_id = st.session_state.user["id"]
data = get_predictions_by_user(user_id)

if not data:
    st.info("No predictions found yet. Go make some predictions first!")
    st.stop()

df = pd.DataFrame([dict(row) for row in data])

total = len(df)
avg_rul = df["predicted_rul"].mean()
critical_count = len(df[df["health_status"] == "Critical"])

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown(f"""
    <div class="stat-card">
        <p class="stat-value">📊 {total}</p>
        <p class="stat-label">Total Predictions</p>
    </div>
    """, unsafe_allow_html=True)
with col_s2:
    st.markdown(f"""
    <div class="stat-card">
        <p class="stat-value">📈 {avg_rul:.1f}</p>
        <p class="stat-label">Average RUL (cycles)</p>
    </div>
    """, unsafe_allow_html=True)
with col_s3:
    st.markdown(f"""
    <div class="stat-card">
        <p class="stat-value">🔴 {critical_count}</p>
        <p class="stat-label">Critical Engines</p>
    </div>
    """, unsafe_allow_html=True)

with st.container(border=True):
    col1, col2 = st.columns([1, 3])
    with col1:
        engine_filter = st.selectbox(
            "🔍 Filter by Engine ID",
            ["All"] + sorted(df["engine_id"].unique().tolist())
        )
    if engine_filter != "All":
        df = df[df["engine_id"] == engine_filter]

def highlight_status(val):
    c = {"Healthy": "background-color: #d4efdf; color: #1e8449",
         "Warning": "background-color: #fdebd0; color: #b9770e",
         "Critical": "background-color: #fadbd8; color: #c0392b"}
    return c.get(val, "")

with st.container(border=True):
    st.subheader("All Predictions")
    display_cols = ["engine_id", "prediction_date", "predicted_rul", "health_status"]
    display_df = df[display_cols].copy()
    display_df["predicted_rul"] = display_df["predicted_rul"].round(2)

    styled = display_df.style.map(highlight_status, subset=["health_status"])
    st.dataframe(styled, width='stretch', hide_index=True,
                 column_config={
                     "engine_id": "Engine ID",
                     "prediction_date": "Date",
                     "predicted_rul": st.column_config.NumberColumn("RUL (cycles)", format="%.1f"),
                     "health_status": "Status",
                 })

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download History", csv,
        "prediction_history.csv", "text/csv",
        width='stretch'
    )

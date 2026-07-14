import streamlit as st
import pandas as pd
from datetime import datetime
from utils.path_setup import *
from utils.styles import inject_global_css, status_badge_html
from utils.sidebar import render_sidebar
from database.queries import (
    get_all_maintenance, get_maintenance_by_engine,
    get_predictions_by_engine, insert_maintenance,
)
from application.reports.theme import HEALTH_COLORS, apply_theme

st.set_page_config(
    page_title="Maintenance Records",
    page_icon="📋",
    layout="wide"
)

inject_global_css()
render_sidebar()

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login first")
    st.stop()

user = st.session_state.user

st.markdown("""
<div class="main-header">
    <h1>📋 Maintenance Records</h1>
    <p>Log new maintenance, investigate engines, and browse all records</p>
</div>
""", unsafe_allow_html=True)

tab_new, tab_drill, tab_all = st.tabs([
    "📝 Log Maintenance", "🔎 Engine Drill-Down", "📋 All Records",
])

with tab_new:
    col_form, col_info = st.columns([2, 3])
    with col_form:
        st.subheader("New Maintenance Record")
        with st.form("maint_form"):
            eid = st.number_input("Engine ID", min_value=1, value=1, step=1,
                                  help="The engine that received maintenance")
            mtype = st.selectbox("Maintenance Type", [
                "Routine Check", "Repair", "Part Replacement",
                "Inspection", "Overhaul", "Other",
            ])
            status = st.selectbox("Status", ["Completed", "Pending"], index=0)
            cost = st.number_input("Cost ($)", min_value=0.0, value=0.0, step=10.0)
            downtime_hours = st.number_input("Downtime (hours)", min_value=0.0, value=0.0, step=0.5)
            notes = st.text_area("Notes (optional)", placeholder="Describe work done, parts used, observations...")
            mdate = st.date_input("Date", value=datetime.now().date())

            submitted = st.form_submit_button("✅ Save Record", type="primary", width='stretch')
            if submitted:
                try:
                    insert_maintenance(
                        engine_id=eid, user_id=user["id"],
                        maintenance_type=mtype, notes=notes,
                        status=status, cost=cost, downtime_hours=downtime_hours,
                        maintenance_date=mdate.strftime("%Y-%m-%d"),
                    )
                    st.toast(f"✅ Maintenance record saved for Engine #{eid}!", icon="✅")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to save: {e}")
    with col_info:
        st.subheader("ℹ️ About Maintenance Types")
        st.markdown("""
        | Type | When to Use |
        |---|---|
        | **Routine Check** | Scheduled periodic inspection |
        | **Repair** | Fixing a specific fault or failure |
        | **Part Replacement** | Swapping a worn/damaged component |
        | **Inspection** | Detailed examination (may involve teardown) |
        | **Overhaul** | Major rebuild or comprehensive service |
        | **Other** | Any maintenance not covered above |
        """)

with tab_drill:
    st.subheader("🔎 Investigate an Engine")
    search_id = st.number_input("Enter Engine ID to inspect", min_value=1,
                                value=1, step=1, key="drill_engine")
    if search_id:
        preds = get_predictions_by_engine(search_id)
        maints = get_maintenance_by_engine(search_id)

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown("#### 🔮 Prediction History")
            if preds:
                pdf = pd.DataFrame(preds)

                def status_bg(val):
                    c = {"Healthy": "#d5f5e3", "Warning": "#fef3cd", "Critical": "#fde8e8"}
                    return f"background-color: {c.get(val, 'transparent')}"

                styled = pdf[["prediction_date", "predicted_rul", "health_status"]].style.map(
                    status_bg, subset=["health_status"]
                )
                st.dataframe(styled, width='stretch', hide_index=True)
                csv_pred = pdf.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download Predictions CSV", csv_pred,
                                   f"engine_{search_id}_predictions.csv",
                                   "text/csv", width='stretch')
            else:
                st.info("No predictions for this engine.")

        with col_d2:
            st.markdown("#### 🛠️ Maintenance History")
            if maints:
                mdf = pd.DataFrame(maints)
                display_maint_cols = [c for c in ["maintenance_date", "maintenance_type", "status", "cost", "downtime_hours", "notes", "engineer_name"] if c in mdf.columns]
                st.dataframe(mdf[display_maint_cols], width='stretch', hide_index=True)
                csv_maint = mdf.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download Maintenance CSV", csv_maint,
                                   f"engine_{search_id}_maintenance.csv",
                                   "text/csv", width='stretch')

                if not preds:
                    pass
            else:
                st.info("No maintenance records for this engine.")

        if preds and maints:
            st.markdown("#### 📈 RUL Trend with Maintenance Events")
            df_pred_sorted = pd.DataFrame(preds).sort_values("prediction_date")
            df_maint_sorted = pd.DataFrame(maints)
            import plotly.graph_objects as go

            fig_rul = go.Figure()
            fig_rul.add_trace(go.Scatter(
                x=df_pred_sorted["prediction_date"],
                y=df_pred_sorted["predicted_rul"],
                mode="lines+markers", name="Predicted RUL",
                line=dict(color="#2E86AB", width=2), marker=dict(size=6)
            ))
            max_rul = df_pred_sorted["predicted_rul"].max()
        for _, row in df_maint_sorted.iterrows():

             fig_rul.add_trace(
              go.Scatter(
                x=[row["maintenance_date"], row["maintenance_date"]],
                y=[0, max_rul],
                mode="lines+text",
                line=dict(
                color=HEALTH_COLORS.get("Warning", "#ff7f0e"),
                dash="dash"
            ),
            text=["", row["maintenance_type"]],
            textposition="top center",
            showlegend=False,
            hovertemplate=f"{row['maintenance_type']}<extra></extra>"
        )
    )
        fig_rul.update_layout(
                title=f"RUL Trend with Maintenance Events - Engine {search_id}",
                xaxis_title="Date", yaxis_title="Predicted RUL (cycles)",
                hovermode="x unified"
            )
        apply_theme(fig_rul)
        st.plotly_chart(fig_rul, width='stretch')

with tab_all:
    st.subheader("📋 All Maintenance Records")
    all_maintenance = get_all_maintenance()
    if all_maintenance:
        mdf_all = pd.DataFrame(all_maintenance)
        display_cols = [c for c in ["engine_id", "maintenance_date", "maintenance_type",
                                     "status", "cost", "downtime_hours", "notes", "full_name"]
                        if c in mdf_all.columns]
        mdf_display = mdf_all[display_cols].copy()
        if "status" in mdf_display.columns:
            mdf_display["status"] = mdf_display["status"].apply(
                lambda x: status_badge_html(x) if pd.notna(x) else x
            )
        st.dataframe(mdf_display, width='stretch')

        csv_all = mdf_all.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download All Records (CSV)", csv_all,
                           "all_maintenance.csv", "text/csv",
                           width='stretch')
    else:
        st.info("📭 No maintenance records yet. Log your first one in the **Log Maintenance** tab!")

import streamlit as st
from utils.path_setup import *
from utils.styles import inject_global_css
from utils.sidebar import render_sidebar

from application.reports.reports import (
    get_dashboard_kpis, get_prediction_summary, get_critical_engines,
    get_maintenance_history, get_recent_predictions, get_engineer_activity,
    get_health_status_distribution, get_prediction_trend,
    get_maintenance_type_distribution, get_maintenance_by_engine
)
from application.reports.charts import (
    create_health_status_chart, create_prediction_trend_chart,
    create_maintenance_type_chart, create_engineer_activity_chart,
    create_critical_engines_chart
)
from application.reports.export import export_to_csv, export_multiple_reports

st.set_page_config(
    page_title="Reports & Analytics",
    page_icon="📊",
    layout="wide"
)

inject_global_css()
render_sidebar()

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login first")
    st.stop()

st.markdown(
    '<div class="main-header"><h1>📊 Reports & Analytics</h1><p>System-wide insights and exportable reports</p></div>',
    unsafe_allow_html=True,
)

col_refresh, _ = st.columns([1, 8])
with col_refresh:
    if st.button("🔄 Refresh"):
        st.rerun()

with st.spinner("Loading reports..."):
    try:
        kpis = get_dashboard_kpis()
        summary = get_prediction_summary()
        df_critical = get_critical_engines()
        df_predictions = get_recent_predictions(100)
        df_maintenance = get_maintenance_history()
        df_engineers = get_engineer_activity()
        df_health = get_health_status_distribution()
        df_trend = get_prediction_trend()
        df_maintenance_types = get_maintenance_type_distribution()
    except Exception as e:
        st.error(f"Error loading reports: {e}")
        st.stop()

with st.container(border=True):
    st.subheader("📈 Prediction Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Average RUL", summary["Average_RUL"])
    c2.metric("Minimum RUL", summary["Minimum_RUL"])
    c3.metric("Maximum RUL", summary["Maximum_RUL"])
    c4.metric("Total Predictions", summary["Total_Predictions"])

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard", "⚠ Critical Engines", "🔮 Predictions",
    "🔧 Maintenance", "📈 Analytics", "📥 Export"
])

with tab1:
    with st.container(border=True):
        st.subheader("System KPIs")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("👥 Users", kpis["users"])
        k2.metric("🤖 Predictions", kpis["predictions"])
        k3.metric("🔧 Maintenance", kpis["maintenance"])
        k4.metric("⚠ Critical Engines", kpis["critical"])

    with st.container(border=True):
        st.subheader("Latest Predictions")
        if df_predictions.empty:
            st.info("No predictions available.")
        else:
            st.dataframe(df_predictions.head(10), width='stretch')

with tab2:
    with st.container(border=True):
        st.subheader("⚠ High Risk Engines")
        if df_critical.empty:
            st.success("✅ No critical engines found.")
        else:
            st.dataframe(df_critical, width='stretch')
            st.download_button(
                "📥 Download Critical Engines CSV", export_to_csv(df_critical),
                "critical_engines.csv", "text/csv", width='stretch'
            )

with tab3:
    with st.container(border=True):
        st.subheader("🔮 Prediction History")
        if df_predictions.empty:
            st.info("No predictions available.")
        else:
            st.dataframe(df_predictions, width='stretch')
            st.download_button(
                "📥 Download Prediction History", export_to_csv(df_predictions),
                "prediction_history.csv", "text/csv", width='stretch'
            )

with tab4:
    with st.container(border=True):
        st.subheader("🔧 Maintenance History")
        engine_id = st.text_input("Search Maintenance by Engine ID", placeholder="Example: 1001")
        if engine_id:
            try:
                search_df = get_maintenance_by_engine(engine_id)
                if search_df.empty:
                    st.warning("No maintenance history found.")
                else:
                    st.success(f"Maintenance History for Engine {engine_id}")
                    st.dataframe(search_df, width='stretch')
            except Exception as e:
                st.error(e)

        st.markdown("---")
        if df_maintenance.empty:
            st.info("No maintenance records available.")
        else:
            st.dataframe(df_maintenance, width='stretch')
            st.download_button(
                "📥 Download Maintenance History", export_to_csv(df_maintenance),
                "maintenance_history.csv", "text/csv", width='stretch'
            )

with tab5:
    st.subheader("📊 Analytics Dashboard")

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("### ❤️ Health Status Distribution")
            fig = create_health_status_chart(df_health)
            if fig:
                st.plotly_chart(fig, width='stretch')
            else:
                st.info("No data available.")

    with col2:
        with st.container(border=True):
            st.markdown("### 📈 Prediction Trend")
            fig = create_prediction_trend_chart(df_trend)
            if fig:
                st.plotly_chart(fig, width='stretch')
            else:
                st.info("No data available.")

    col3, col4 = st.columns(2)
    with col3:
        with st.container(border=True):
            st.markdown("### 🔧 Maintenance Types")
            fig = create_maintenance_type_chart(df_maintenance_types)
            if fig:
                st.plotly_chart(fig, width='stretch')
            else:
                st.info("No data available.")

    with col4:
        with st.container(border=True):
            st.markdown("### 👷 Engineer Activity")
            fig = create_engineer_activity_chart(df_engineers)
            if fig:
                st.plotly_chart(fig, width='stretch')
            else:
                st.info("No data available.")

    with st.container(border=True):
        st.markdown("### 🚨 Critical Engines Overview")
        fig = create_critical_engines_chart(df_critical)
        if fig:
            st.plotly_chart(fig, width='stretch')
        else:
            st.success("No critical engines detected.")

with tab6:
    with st.container(border=True):
        st.subheader("📥 Export Reports")
        st.info("Download all system reports as a single Excel workbook.")

        report_dict = {
            "Critical Engines": df_critical,
            "Prediction History": df_predictions,
            "Maintenance History": df_maintenance,
            "Engineer Activity": df_engineers
        }
        excel = export_multiple_reports(report_dict)

        st.download_button(
            "📥 Download Full Excel Report", data=excel,
            file_name="AI_Maintenance_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width='stretch'
        )

        st.markdown("---")
        st.write("Download individual reports:")

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("Critical Engines CSV", export_to_csv(df_critical),
                               "critical_engines.csv", "text/csv", width='stretch')
            st.download_button("Prediction History CSV", export_to_csv(df_predictions),
                               "prediction_history.csv", "text/csv", width='stretch')
        with col2:
            st.download_button("Maintenance History CSV", export_to_csv(df_maintenance),
                               "maintenance_history.csv", "text/csv", width='stretch')
            st.download_button("Engineer Activity CSV", export_to_csv(df_engineers),
                               "engineer_activity.csv", "text/csv", width='stretch')

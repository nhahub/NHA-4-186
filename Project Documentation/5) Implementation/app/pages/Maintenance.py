import streamlit as st
import pandas as pd
from utils.path_setup import *
from utils.styles import inject_global_css
from utils.sidebar import render_sidebar
from database.queries import (
    get_latest_prediction_per_engine, get_all_maintenance,
    get_maintenance_count, get_engines_with_maintenance,
    get_recent_maintenance,
)
from application.reports.reports import get_maintenance_type_distribution
from application.reports.charts import create_maintenance_type_chart

st.set_page_config(
    page_title="Maintenance Dashboard",
    page_icon="🛠️",
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
    <h1>🛠️ Maintenance Dashboard</h1>
    <p>Real-time fleet health & maintenance command center — prioritize, act, track.</p>
</div>
""", unsafe_allow_html=True)

engine_statuses = get_latest_prediction_per_engine()
all_maintenance = get_all_maintenance()
maintenance_types = get_maintenance_type_distribution()
recent_maintenance = get_recent_maintenance(10)
total_maint = get_maintenance_count()
engines_serviced = get_engines_with_maintenance()

critical_engines = [e for e in engine_statuses if e["health_status"] == "Critical"]
warning_engines = [e for e in engine_statuses if e["health_status"] == "Warning"]
healthy_engines = [e for e in engine_statuses if e["health_status"] == "Healthy"]
avg_rul = (
    sum(e["predicted_rul"] for e in engine_statuses) / len(engine_statuses)
    if engine_statuses else 0
)
fleet_size = len(engine_statuses)

if st.button("🔄 Refresh", type="secondary"):
    st.rerun()

st.markdown("### 📊 Fleet Overview")
col_a, col_b, col_c, col_d, col_e = st.columns(5)
with col_a:
    st.markdown(f"""
    <div class="stat-card {'critical' if critical_engines else 'info'}">
        <p class="stat-value">🔴 {len(critical_engines)}</p>
        <p class="stat-label">Critical Engines</p>
    </div>
    """, unsafe_allow_html=True)
with col_b:
    st.markdown(f"""
    <div class="stat-card {'warning' if warning_engines else 'info'}">
        <p class="stat-value">⚠️ {len(warning_engines)}</p>
        <p class="stat-label">Warnings</p>
    </div>
    """, unsafe_allow_html=True)
with col_c:
    st.markdown(f"""
    <div class="stat-card success">
        <p class="stat-value">✅ {len(healthy_engines)}</p>
        <p class="stat-label">Healthy</p>
    </div>
    """, unsafe_allow_html=True)
with col_d:
    st.markdown(f"""
    <div class="stat-card">
        <p class="stat-value">📈 {avg_rul:.0f}</p>
        <p class="stat-label">Avg RUL (cycles)</p>
    </div>
    """, unsafe_allow_html=True)
with col_e:
    st.markdown(f"""
    <div class="stat-card">
        <p class="stat-value">🏭 {fleet_size}</p>
        <p class="stat-label">Engines Tracked</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

col_left, col_right = st.columns([3, 2])

with col_left:
    tab_fleet, tab_critical_tab = st.tabs(["🚀 Fleet Health", "🔴 Priority Queue"])

    with tab_fleet:
        if not engine_statuses:
            st.info("📭 No engine predictions yet. Make predictions first on the **Prediction** page.")

        total_engines = len(engine_statuses)
        if total_engines > 0:
            healthy_pct = len(healthy_engines) / total_engines * 100
            warn_pct = len(warning_engines) / total_engines * 100
            crit_pct = len(critical_engines) / total_engines * 100

            st.markdown(f"""
            <div style="display:flex; height:24px; border-radius:12px; overflow:hidden; margin-bottom:1rem;">
                <div style="width:{healthy_pct:.1f}%; background:#2ecc71; display:flex; align-items:center; justify-content:center; color:white; font-size:0.7rem; font-weight:700;">
                    {len(healthy_engines)} Healthy
                </div>
                <div style="width:{warn_pct:.1f}%; background:#f39c12; display:flex; align-items:center; justify-content:center; color:white; font-size:0.7rem; font-weight:700;">
                    {len(warning_engines)} Warn
              </div>
                <div style="width:{crit_pct:.1f}%; background:#e74c3c; display:flex; align-items:center; justify-content:center; color:white; font-size:0.7rem; font-weight:700;">
                    {len(critical_engines)} Crit
                </div>
            </div>
            """, unsafe_allow_html=True)

        sorted_engines = sorted(engine_statuses, key=lambda e: (
            {"Critical": 0, "Warning": 1, "Healthy": 2}.get(e["health_status"], 3),
            e["predicted_rul"],
        ))

        for eng in sorted_engines:
            status = eng["health_status"]
            css_class = {"Critical": "critical", "Warning": "warning", "Healthy": "healthy"}.get(status, "")
            badge_class = {"Critical": "badge-critical", "Warning": "badge-warning", "Healthy": "badge-healthy"}.get(status, "")
            emoji = {"Critical": "🔴", "Warning": "🟡", "Healthy": "🟢"}.get(status, "⚪")
            rul = eng["predicted_rul"]
            rul_normalized = min(rul / 300 * 100, 100)
            bar_color = {"Critical": "#e74c3c", "Warning": "#f39c12", "Healthy": "#2ecc71"}.get(status, "#ccc")

            st.markdown(f"""
            <div class="engine-card {css_class}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <strong style="font-size:1.05rem;">{emoji} Engine #{eng['engine_id']}</strong>
                        <span class="badge {badge_class}" style="margin-left:0.6rem;">{status}</span>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:1.2rem; font-weight:700;">{rul:.1f}</span>
                        <span class="text-muted" style="font-size:0.8rem;"> cycles left</span>
                    </div>
                </div>
                <div class="rul-bar-container" style="margin-top:0.5rem;">
                    <div class="rul-bar-fill" style="width:{rul_normalized:.1f}%; background:{bar_color};"></div>
                </div>
                <div class="text-xs text-muted" style="margin-top:0.25rem;">
                    Last predicted: {eng.get('prediction_date', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_critical_tab:
        if critical_engines:
            st.warning(f"🚨 **{len(critical_engines)} engine(s) need immediate attention!**")
            crit_sorted = sorted(critical_engines, key=lambda e: e["predicted_rul"])
            for i, eng in enumerate(crit_sorted):
                urgency = "🚨 IMMEDIATE" if eng["predicted_rul"] < 15 else "⚠️ URGENT"
                st.markdown(f"""
                <div class="engine-card critical" style="margin-bottom:0.8rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span class="text-critical fw-800" style="font-size:1.3rem;">#{i+1}</span>
                            <strong style="margin-left:0.5rem;">Engine #{eng['engine_id']}</strong>
                            <span class="badge badge-critical">{urgency}</span>
                        </div>
                        <div style="text-align:right;">
                            <span class="text-critical fw-800" style="font-size:1.4rem;">{eng['predicted_rul']:.1f}</span>
                            <span class="text-muted"> cycles</span>
                        </div>
                    </div>
                    <div class="text-sm text-muted" style="margin-top:0.3rem;">
                        Last predicted: {eng.get('prediction_date', 'N/A')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        elif warning_engines:
            st.info(f"⚠️ No critical engines, but {len(warning_engines)} engine(s) are in Warning status. Plan maintenance soon.")
            for eng in sorted(warning_engines, key=lambda e: e["predicted_rul"])[:5]:
                st.markdown(f"""
                <div class="engine-card warning">
                    <strong>⚠️ Engine #{eng['engine_id']}</strong> — {eng['predicted_rul']:.1f} cycles remaining
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🎉 All engines are healthy! No priority actions needed.")

with col_right:
    st.markdown('<div class="section-title">⚡ Quick Actions</div>', unsafe_allow_html=True)

    col_qa1, col_qa2 = st.columns(2)
    with col_qa1:
        st.page_link("pages/Prediction.py", label="🔮 New Prediction", icon="🔮")
    with col_qa2:
        if st.button("🔄 Refresh Data", width='stretch'):
            st.rerun()

    st.divider()

    st.markdown('<div class="section-title">📊 Maintenance Stats</div>', unsafe_allow_html=True)

    col_ms1, col_ms2 = st.columns(2)
    with col_ms1:
        st.metric("Total Records", total_maint, border=True)
    with col_ms2:
        st.metric("Engines Serviced", engines_serviced, border=True)

    if maintenance_types is not None and not maintenance_types.empty:
        fig = create_maintenance_type_chart(maintenance_types)
        if fig:
            fig.update_layout(height=200, margin=dict(t=20, b=10, l=10, r=10))
            st.plotly_chart(fig, width='stretch')

    st.divider()

    st.markdown('<div class="section-title">🕐 Recent Activity</div>', unsafe_allow_html=True)

    if recent_maintenance:
        for rec in recent_maintenance[:5]:
            mt = rec["maintenance_type"]
            eid = rec["engine_id"]
            date = rec["maintenance_date"][:10] if rec["maintenance_date"] else "N/A"
            eng_name = rec.get("engineer_name", "Unknown")
            st.markdown(f"""
            <div class="engine-card" style="padding:0.6rem 0.8rem; font-size:0.85rem;">
                <strong>🔧 {mt}</strong> — Engine #{eid}<br>
                <span class="text-muted">{date} · by {eng_name}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No maintenance records yet.")

st.divider()

st.markdown("### 🔍 Need More Detail?")
st.info("Log new maintenance, investigate specific engines, and browse all records on the dedicated **Maintenance Records** page.")
st.page_link("pages/Maintenance_Records.py", label="📋 Open Maintenance Records", icon="📋")

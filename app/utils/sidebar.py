import streamlit as st
from utils.styles import role_badge_html


def render_sidebar():
    if "user" not in st.session_state or st.session_state.user is None:
        return

    user = st.session_state.user

    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-user">
                <div class="avatar">👤</div>
                <div class="name">{user['full_name']}</div>
                <div class="username">@{user['username']}</div>
                <div style="margin-top: 0.4rem;">{role_badge_html(user['role'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### Navigation")

        if st.button("🔮 Prediction", key="nav_prediction", width='stretch'):
            st.switch_page("pages/Prediction.py")
        if st.button("📜 History", key="nav_history", width='stretch'):
            st.switch_page("pages/History.py")
        if st.button("🔧 Maintenance", key="nav_maintenance", width='stretch'):
            st.switch_page("pages/Maintenance.py")
        if st.button("📋 Records", key="nav_records", width='stretch'):
            st.switch_page("pages/Maintenance_Records.py")
        if st.button("📊 Reports", key="nav_reports", width='stretch'):
            st.switch_page("pages/Reports.py")

        st.markdown("---")

        theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
        theme_label = "Dark Mode" if st.session_state.theme == "light" else "Light Mode"
        if st.button(f"{theme_icon} {theme_label}", key="nav_theme", width='stretch'):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()

        if st.button("🚪 Logout", key="nav_logout", width='stretch', type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        st.markdown(
            '<div class="sidebar-footer">AI Predictive Maintenance v1.0</div>',
            unsafe_allow_html=True,
        )

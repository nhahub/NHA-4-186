import streamlit as st
import sys
from pathlib import Path
from utils.path_setup import *
from utils.styles import inject_global_css
from application.auth.service import AuthService

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

st.set_page_config(
    page_title="AI Predictive Maintenance",
    page_icon="🔧",
    layout="centered"
)

inject_global_css()

auth = AuthService()

if "user" not in st.session_state:
    st.session_state.user = None

st.markdown(
    """
    <div class="main-header" style="text-align:center;">
        <h1>🔧 AI Predictive Maintenance</h1>
        <p>Login or create an account to get started</p>
    </div>
    """,
    unsafe_allow_html=True,
)

login_tab, signup_tab = st.tabs(["🔐 Login", "📝 Sign Up"])

with login_tab:
    with st.container(border=True):
        st.subheader("Welcome Back")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", width='stretch'):
            success, result = auth.login(username, password)
            if success:
                st.session_state.user = {
                    "id": result["id"],
                    "full_name": result["full_name"],
                    "username": result["username"],
                    "role": result["role"]
                }
                st.toast(f"Welcome {result['full_name']} 👋", icon="👋")
                st.switch_page("pages/Prediction.py")
            else:
                st.error(result)

with signup_tab:
    with st.container(border=True):
        st.subheader("Create Account")
        full_name = st.text_input("Full Name", key="register_full_name")
        username = st.text_input("Username", key="register_username")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")

        st.info("New accounts are created as Engineer.")
        role = "Engineer"

        if st.button("Create Account", width='stretch'):
            success, message = auth.register(full_name, username, email, password, role)
            if success:
                st.toast(f"✅ {message}", icon="✅")
            else:
                st.error(message)

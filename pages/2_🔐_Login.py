"""
User and admin login page.
"""
import streamlit as st
from backend.auth.authentication import AuthenticationManager
from backend.user.user_manager import UserManager
from database.db_manager import DatabaseManager
import config

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

if st.session_state.get('logged_in', False):
    st.success(f"Already logged in as {st.session_state.user_name}")
    if st.button("🏠 Go Home"):
        st.switch_page("app.py")
    st.stop()

st.title("🔐 Login")

tab1, tab2 = st.tabs(["👤 Customer Login", "👨‍💼 Admin Login"])

with tab1:
    with st.form("customer_login"):
        st.markdown("### Customer Login")
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("🔓 Login", use_container_width=True, type="primary")
        with col2:
            home_btn = st.form_submit_button("🏠 Home", use_container_width=True)
        
        if home_btn:
            st.switch_page("app.py")
        
        if submit:
            if not email or not password:
                st.error("Please fill all fields")
            else:
                success, user_id, message = AuthenticationManager.login_user(email, password)
                if success:
                    user = UserManager.get_user_profile(user_id)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.user_name = f"{user['first_name']} {user['last_name']}"
                        st.session_state.user_email = email
                        st.session_state.is_admin = False
                        DatabaseManager.log_action(user_id, 'user_login', f'User {email} logged in')
                        st.success(message)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("User profile not found")
                else:
                    st.error(message)
    
    st.markdown("---")
    if st.button("📝 Don't have account? Register", use_container_width=True):
        st.switch_page("pages/3_📝_Register.py")

with tab2:
    with st.form("admin_login"):
        st.markdown("### Admin Login")
        st.warning("⚠️ Staff only")
        username = st.text_input("Username")
        admin_password = st.text_input("Password", type="password", key="admin_pass")
        
        col1, col2 = st.columns(2)
        with col1:
            admin_submit = st.form_submit_button("🔓 Login", use_container_width=True, type="primary")
        with col2:
            admin_home = st.form_submit_button("🏠 Home", use_container_width=True)
        
        if admin_home:
            st.switch_page("app.py")
        
        if admin_submit:
            if not username or not admin_password:
                st.error("Please fill all fields")
            else:
                success, admin_id, role, message = AuthenticationManager.login_admin(username, admin_password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.is_admin = True
                    st.session_state.admin_id = admin_id
                    st.session_state.admin_role = role
                    st.session_state.user_name = username
                    st.success(f"{message} - Role: {role.upper()}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(message)

"""
User registration page.
"""
import streamlit as st
from backend.auth.authentication import AuthenticationManager
from utils.validators import validate_email, validate_password, validate_phone_number
import config

st.set_page_config(page_title="Register", page_icon="📝", layout="centered")

if st.session_state.get('logged_in', False):
    st.info("Already logged in")
    if st.button("🏠 Home"):
        st.switch_page("app.py")
    st.stop()

st.title("📝 Create Account")

with st.form("registration"):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name *")
    with col2:
        last_name = st.text_input("Last Name *")
    
    email = st.text_input("Email *")
    phone = st.text_input("Phone *", placeholder="+1234567890")
    password = st.text_input("Password *", type="password")
    confirm_password = st.text_input("Confirm Password *", type="password")
    
    st.info("""
    **Password Requirements:**
    - At least 8 characters
    - Uppercase and lowercase letters
    - Numbers
    """)
    
    agree = st.checkbox("I agree to Terms & Conditions *")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        submit = st.form_submit_button("✅ Register", use_container_width=True, type="primary")
    with col2:
        login_btn = st.form_submit_button("🔐 Login", use_container_width=True)
    with col3:
        home_btn = st.form_submit_button("🏠 Home", use_container_width=True)
    
    if login_btn:
        st.switch_page("pages/2_🔐_Login.py")
    if home_btn:
        st.switch_page("app.py")
    
    if submit:
        errors = []
        if not all([first_name, last_name, email, phone, password]):
            errors.append("All fields required")
        if email and not validate_email(email):
            errors.append("Invalid email")
        if phone and not validate_phone_number(phone):
            errors.append("Invalid phone number")
        if password and not validate_password(password):
            errors.append("Password doesn't meet requirements")
        if password != confirm_password:
            errors.append("Passwords don't match")
        if not agree:
            errors.append("Must agree to terms")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            success, message = AuthenticationManager.register_user(
                email, password, first_name, last_name, phone
            )
            if success:
                st.success(message)
                st.balloons()
                st.info("Redirecting to login...")
                import time
                time.sleep(2)
                st.switch_page("pages/2_🔐_Login.py")
            else:
                st.error(message)

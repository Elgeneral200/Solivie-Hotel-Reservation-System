"""
User registration page.
UPDATED: Added National ID/Passport collection
"""
import streamlit as st
from backend.auth.authentication import AuthenticationManager
from utils.validators import validate_email, validate_password, validate_phone_number
from datetime import date
import config

st.set_page_config(page_title="Register", page_icon="📝", layout="centered")

if st.session_state.get('logged_in', False):
    st.info("Already logged in")
    if st.button("🏠 Home"):
        st.switch_page("app.py")
    st.stop()

st.title("📝 Create Account")

with st.form("registration"):
    # ===== PERSONAL INFORMATION =====
    st.markdown("### 👤 Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name *", key="reg_fname")
    with col2:
        last_name = st.text_input("Last Name *", key="reg_lname")
    
    email = st.text_input("Email *", key="reg_email")
    phone = st.text_input("Phone *", placeholder="+1234567890", key="reg_phone")
    
    st.markdown("---")
    
    # ===== NEW: IDENTIFICATION SECTION =====
    st.markdown("### 🆔 Identification (Required for Hotel Check-in)")
    st.caption("⚠️ This information is required by law for hotel bookings")
    
    col1, col2 = st.columns(2)
    with col1:
        id_type = st.selectbox(
            "ID Type *", 
            ["National ID", "Passport"], 
            key="reg_id_type",
            help="Select your identification document type"
        )
    with col2:
        if id_type == "National ID":
            id_number = st.text_input(
                "National ID Number *", 
                key="reg_id_num",
                placeholder="Enter your National ID"
            )
        else:
            id_number = st.text_input(
                "Passport Number *", 
                key="reg_passport",
                placeholder="Enter your Passport number"
            )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        nationality = st.selectbox(
            "Nationality *", 
            [
                "Egypt", "Saudi Arabia", "UAE", "Qatar", "Kuwait",
                "USA", "UK", "France", "Germany", "Italy", 
                "Spain", "Canada", "Australia", "Japan", "China",
                "India", "Brazil", "Mexico", "Other"
            ], 
            key="reg_nationality"
        )
    with col2:
        dob = st.date_input(
            "Date of Birth *", 
            min_value=date(1920, 1, 1), 
            max_value=date.today(),
            value=date(1990, 1, 1),
            key="reg_dob",
            help="Your date of birth as per ID"
        )
    with col3:
        id_expiry = st.date_input(
            "ID Expiry Date *",
            min_value=date.today(),
            value=date(2030, 12, 31),
            key="reg_expiry",
            help="When does your ID expire?"
        )
    
    st.markdown("---")
    
    # ===== SECURITY =====
    st.markdown("### 🔒 Security")
    password = st.text_input("Password *", type="password", key="reg_pass1")
    confirm_password = st.text_input("Confirm Password *", type="password", key="reg_pass2")
    
    st.info("""
    **Password Requirements:**
    - At least 8 characters
    - Uppercase and lowercase letters
    - Numbers
    """)
    
    agree = st.checkbox("I agree to Terms & Conditions and Privacy Policy *", key="reg_agree")
    
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
        
        # UPDATED: Validate all fields including ID
        if not all([first_name, last_name, email, phone, password, id_number, nationality]):
            errors.append("❌ All required fields must be filled")
        if email and not validate_email(email):
            errors.append("❌ Invalid email format")
        if phone and not validate_phone_number(phone):
            errors.append("❌ Invalid phone number format")
        if password and not validate_password(password):
            errors.append("❌ Password doesn't meet requirements")
        if password != confirm_password:
            errors.append("❌ Passwords don't match")
        if not agree:
            errors.append("❌ Must agree to terms and conditions")
        
        # Validate ID expiry is in the future
        if id_expiry <= date.today():
            errors.append("❌ ID expiry date must be in the future")
        
        # Validate age (must be 18+)
        age = (date.today() - dob).days // 365
        if age < 18:
            errors.append("❌ You must be at least 18 years old to register")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # UPDATED: Register with ID information
            success, message = AuthenticationManager.register_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone,
                # NEW: ID parameters
                national_id=id_number if id_type == "National ID" else None,
                passport_number=id_number if id_type == "Passport" else None,
                nationality=nationality,
                date_of_birth=dob,
                id_expiry_date=id_expiry
            )
            if success:
                st.success(f"✅ {message}")
                st.balloons()
                st.info("📧 Redirecting to login...")
                import time
                time.sleep(2)
                st.switch_page("pages/2_🔐_Login.py")
            else:
                st.error(f"❌ {message}")

"""
User Registration Page - Dark Luxury Theme
Enhanced with Solivie Hotel design system
UPDATED: Includes National ID/Passport collection
"""
import streamlit as st
from backend.auth.authentication import AuthenticationManager
from utils.validators import validate_email, validate_password, validate_phone_number
from utils.ui_components import SolivieUI
from datetime import date
import config


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Register - Solivie Hotel",
    page_icon="📝",
    layout="centered"
)

# Apply dark luxury CSS
SolivieUI.inject_custom_css()

# Enhanced button styling for ALL button types
st.markdown("""
<style>
/* Force all regular buttons */
.stButton > button,
.stButton button,
div[data-testid="stButton"] > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.5px !important;
    transition: all 0.4s ease !important;
    text-transform: uppercase !important;
    font-size: 0.9rem !important;
    border: none !important;
}

/* Primary buttons - Gold gradient */
.stButton > button[kind="primary"],
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #C4935B 0%, #B8875A 100%) !important;
    color: #1A1F1E !important;
    box-shadow: 0 4px 15px rgba(196, 147, 91, 0.3) !important;
}

.stButton > button[kind="primary"]:hover,
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(196, 147, 91, 0.5) !important;
    background: linear-gradient(135deg, #D4A76A 0%, #C4935B 100%) !important;
}

/* Secondary buttons - Gold border */
.stButton > button[kind="secondary"],
div[data-testid="stButton"] > button[kind="secondary"] {
    background: transparent !important;
    color: #C4935B !important;
    border: 2px solid #C4935B !important;
}

.stButton > button[kind="secondary"]:hover,
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: rgba(196, 147, 91, 0.1) !important;
    border-color: #D4A76A !important;
    color: #D4A76A !important;
    transform: translateY(-2px) !important;
}

/* Form submit buttons - CRITICAL FIX */
.stForm button[kind="primary"],
button[data-testid="stFormSubmitButton"],
.stForm button[type="submit"] {
    background: linear-gradient(135deg, #C4935B 0%, #B8875A 100%) !important;
    color: #1A1F1E !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(196, 147, 91, 0.3) !important;
}

.stForm button[kind="primary"]:hover,
button[data-testid="stFormSubmitButton"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(196, 147, 91, 0.5) !important;
    background: linear-gradient(135deg, #D4A76A 0%, #C4935B 100%) !important;
}

/* Form secondary buttons */
.stForm button[kind="secondary"] {
    background: transparent !important;
    color: #C4935B !important;
    border: 2px solid #C4935B !important;
    border-radius: 10px !important;
}

.stForm button[kind="secondary"]:hover {
    background: rgba(196, 147, 91, 0.1) !important;
    border-color: #D4A76A !important;
    color: #D4A76A !important;
}

/* Default form buttons (no type specified) */
.stForm button {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%) !important;
    color: #F5F5F0 !important;
    border: 2px solid #3D4A47 !important;
    border-radius: 10px !important;
}

.stForm button:hover {
    border-color: #C4935B !important;
    transform: translateY(-2px) !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# CHECK IF ALREADY LOGGED IN
# ============================================================================

if st.session_state.get('logged_in', False):
    st.markdown("""
    <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                border: 2px solid #6B8E7E;
                margin: 2rem 0;'>
        <h2 style='color: #6B8E7E; margin: 0 0 1rem 0;'>✅ Already Logged In</h2>
        <p style='color: #F5F5F0; font-size: 1.2rem; margin: 0;'>
            You're already signed in!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🏠 GO TO HOME", use_container_width=True, type="primary", key="already_logged_home"):
            st.switch_page("app.py")
    st.stop()


# ============================================================================
# PAGE HEADER
# ============================================================================

SolivieUI.page_header(
    "Create Your Account",
    "Join Solivie Hotel and unlock exclusive member benefits",
    "📝"
)


# ============================================================================
# REGISTRATION FORM
# ============================================================================

with st.form("registration", clear_on_submit=False):
    
    # ===== PERSONAL INFORMATION SECTION =====
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 1.5rem;'>
        <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 1.5rem;'>
            👤 Personal Information
        </h3>
        <p style='color: #9BA8A5; margin: 0;'>
            Tell us about yourself
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input(
            "First Name *",
            placeholder="John",
            key="reg_fname"
        )
    
    with col2:
        last_name = st.text_input(
            "Last Name *",
            placeholder="Doe",
            key="reg_lname"
        )
    
    email = st.text_input(
        "Email Address *",
        placeholder="your@email.com",
        key="reg_email"
    )
    
    phone = st.text_input(
        "Phone Number *",
        placeholder="+1 (555) 123-4567",
        key="reg_phone"
    )
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # ===== IDENTIFICATION SECTION =====
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 1.5rem;'>
        <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 1.5rem;'>
            🆔 Identification
        </h3>
        <p style='color: #9BA8A5; margin: 0;'>
            Required by law for hotel bookings
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                padding: 1rem;
                border-radius: 10px;
                border: 2px solid #C4935B;
                margin-bottom: 1.5rem;'>
        <p style='color: #D4A76A; margin: 0; font-size: 0.9rem;'>
            ⚠️ <strong>Important:</strong> This information is mandatory for hotel check-in verification
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # ===== SECURITY SECTION =====
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 1.5rem;'>
        <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 1.5rem;'>
            🔒 Account Security
        </h3>
        <p style='color: #9BA8A5; margin: 0;'>
            Create a strong password to protect your account
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    password = st.text_input(
        "Password *",
        type="password",
        placeholder="Enter strong password",
        key="reg_pass1"
    )
    
    confirm_password = st.text_input(
        "Confirm Password *",
        type="password",
        placeholder="Re-enter password",
        key="reg_pass2"
    )
    
    # Password requirements card
    st.markdown("""
    <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border: 2px solid #7B9CA8;
                margin: 1rem 0;'>
        <h4 style='color: #7B9CA8; margin: 0 0 0.5rem 0; font-size: 1rem;'>
            🔑 Password Requirements:
        </h4>
        <ul style='color: #9BA8A5; margin: 0; padding-left: 1.5rem; line-height: 1.8;'>
            <li>At least 8 characters long</li>
            <li>Contains uppercase and lowercase letters</li>
            <li>Includes numbers</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Terms & Conditions
    agree = st.checkbox(
        "I agree to the Terms & Conditions and Privacy Policy *",
        key="reg_agree"
    )
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # ===== ACTION BUTTONS =====
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        submit = st.form_submit_button(
            "✅ CREATE ACCOUNT",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        login_btn = st.form_submit_button(
            "🔐 LOGIN",
            use_container_width=True
        )
    
    with col3:
        home_btn = st.form_submit_button(
            "🏠 HOME",
            use_container_width=True
        )
    
    # Handle navigation buttons
    if login_btn:
        st.switch_page("pages/2_🔐_Login.py")
    
    if home_btn:
        st.switch_page("app.py")
    
    # Handle registration submission
    if submit:
        errors = []
        
        # Validate all required fields
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
        
        # Display errors or process registration
        if errors:
            for error in errors:
                st.error(error)
        else:
            with st.spinner("🔄 Creating your account..."):
                # Register with ID information
                success, message = AuthenticationManager.register_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone,
                    # ID parameters
                    national_id=id_number if id_type == "National ID" else None,
                    passport_number=id_number if id_type == "Passport" else None,
                    nationality=nationality,
                    date_of_birth=dob,
                    id_expiry_date=id_expiry
                )
                
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                    
                    # Success message card
                    st.markdown("""
                    <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                                padding: 2rem;
                                border-radius: 15px;
                                text-align: center;
                                border: 2px solid #6B8E7E;
                                margin: 1.5rem 0;'>
                        <h3 style='color: #6B8E7E; margin: 0 0 0.5rem 0;'>
                            🎉 Welcome to Solivie Hotel!
                        </h3>
                        <p style='color: #9BA8A5; margin: 0;'>
                            Redirecting you to login...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    import time
                    time.sleep(2)
                    st.switch_page("pages/2_🔐_Login.py")
                else:
                    st.error(f"❌ {message}")


# ============================================================================
# FOOTER - ALREADY HAVE ACCOUNT
# ============================================================================

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 2rem;
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            border-radius: 15px;
            border: 2px solid #3D4A47;'>
    <p style='color: #9BA8A5; margin: 0 0 1rem 0; font-size: 1rem;'>
        Already have an account?
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

if st.button("🔐 LOGIN TO YOUR ACCOUNT", use_container_width=True, type="secondary", key="bottom_login_btn"):
    st.switch_page("pages/2_🔐_Login.py")

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Privacy & Security notice
st.markdown("""
<div style='text-align: center; padding: 1.5rem;
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            border-radius: 12px;
            border: 2px solid #3D4A47;'>
    <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem;'>
        🔒 Your information is protected with bank-level encryption
    </p>
    <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.85rem;'>
        Questions? Contact <span style='color: #C4935B;'>support@solivie.com</span>
    </p>
</div>
""", unsafe_allow_html=True)

"""
User and Admin Login Page - Dark Luxury Theme
Enhanced with Solivie Hotel design system
FIXED: Button styling + Welcome message interpolation
"""
import streamlit as st
from backend.auth.authentication import AuthenticationManager
from backend.user.user_manager import UserManager
from database.db_manager import DatabaseManager
from utils.ui_components import SolivieUI
import config


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Login - Solivie Hotel",
    page_icon="🔐",
    layout="centered"
)

# Apply dark luxury CSS
SolivieUI.inject_custom_css()

# Enhanced button styling - CRITICAL FIX
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
    # FIXED: Use f-string for proper variable interpolation
    st.markdown(f"""
    <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                border: 2px solid #6B8E7E;
                margin: 2rem 0;'>
        <h2 style='color: #6B8E7E; margin: 0 0 1rem 0;'>✅ Already Logged In</h2>
        <p style='color: #F5F5F0; font-size: 1.2rem; margin: 0;'>
            Welcome back, <strong>{st.session_state.user_name}</strong>!
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
    "Login to Your Account",
    "Access your bookings and exclusive member benefits",
    "🔐"
)


# ============================================================================
# LOGIN TABS
# ============================================================================

tab1, tab2 = st.tabs(["👤 Customer Login", "👨‍💼 Admin Login"])


# ============================================================================
# TAB 1: CUSTOMER LOGIN
# ============================================================================

with tab1:
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Login Card
    st.markdown("""
    <div class='solivie-card' style='max-width: 500px; margin: 0 auto;'>
        <h3 style='color: #C4935B; margin-top: 0; text-align: center; font-size: 1.8rem;'>
            Welcome Back!
        </h3>
        <p style='color: #9BA8A5; text-align: center; margin-bottom: 2rem;'>
            Sign in to access your bookings and profile
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    with st.form("customer_login", clear_on_submit=False):
        email = st.text_input(
            "📧 Email Address",
            placeholder="your@email.com",
            key="customer_email"
        )
        
        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Enter your password",
            key="customer_password"
        )
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            submit = st.form_submit_button(
                "🔓 LOGIN",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            home_btn = st.form_submit_button(
                "🏠 HOME",
                use_container_width=True
            )
        
        # Handle Home button
        if home_btn:
            st.switch_page("app.py")
        
        # Handle Login
        if submit:
            if not email or not password:
                st.error("❌ Please fill in all fields")
            else:
                with st.spinner("🔄 Authenticating..."):
                    success, user_id, message = AuthenticationManager.login_user(email, password)
                    
                    if success:
                        user = UserManager.get_user_profile(user_id)
                        if user:
                            # Set session state
                            st.session_state.logged_in = True
                            st.session_state.user_id = user_id
                            st.session_state.user_name = f"{user['first_name']} {user['last_name']}"
                            st.session_state.user_email = email
                            st.session_state.is_admin = False
                            
                            # Log action
                            DatabaseManager.log_action(
                                user_id,
                                'user_login',
                                f'User {email} logged in'
                            )
                            
                            st.success(f"✅ {message}")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ User profile not found")
                    else:
                        st.error(f"❌ {message}")
    
    # Register prompt
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem;
                background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                border-radius: 12px;
                border: 2px solid #3D4A47;'>
        <p style='color: #9BA8A5; margin: 0 0 1rem 0; font-size: 1rem;'>
            Don't have an account yet?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    
    if st.button("📝 CREATE NEW ACCOUNT", use_container_width=True, type="secondary", key="goto_register"):
        st.switch_page("pages/3_📝_Register.py")


# ============================================================================
# TAB 2: ADMIN LOGIN
# ============================================================================

with tab2:
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Admin Warning Card
    st.markdown("""
    <div style='background: linear-gradient(145deg, #3D2A2A 0%, #2C2020 100%);
                padding: 1.5rem;
                border-radius: 12px;
                text-align: center;
                border: 2px solid #A95F5F;
                margin-bottom: 1.5rem;'>
        <h4 style='color: #D4A76A; margin: 0;'>⚠️ STAFF ACCESS ONLY</h4>
        <p style='color: #9BA8A5; margin: 0.5rem 0 0 0;'>
            Authorized personnel only. Unauthorized access is prohibited.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin Login Card
    st.markdown("""
    <div class='solivie-card' style='max-width: 500px; margin: 0 auto;'>
        <h3 style='color: #C4935B; margin-top: 0; text-align: center; font-size: 1.8rem;'>
            Admin Portal
        </h3>
        <p style='color: #9BA8A5; text-align: center; margin-bottom: 2rem;'>
            Management system access
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    with st.form("admin_login", clear_on_submit=False):
        username = st.text_input(
            "👤 Admin Username",
            placeholder="Enter admin username",
            key="admin_username"
        )
        
        admin_password = st.text_input(
            "🔒 Admin Password",
            type="password",
            placeholder="Enter admin password",
            key="admin_pass"
        )
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            admin_submit = st.form_submit_button(
                "🔓 LOGIN",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            admin_home = st.form_submit_button(
                "🏠 HOME",
                use_container_width=True
            )
        
        # Handle Home button
        if admin_home:
            st.switch_page("app.py")
        
        # Handle Admin Login
        if admin_submit:
            if not username or not admin_password:
                st.error("❌ Please fill in all fields")
            else:
                with st.spinner("🔄 Verifying credentials..."):
                    success, admin_id, role, message = AuthenticationManager.login_admin(
                        username,
                        admin_password
                    )
                    
                    if success:
                        # Set session state
                        st.session_state.logged_in = True
                        st.session_state.is_admin = True
                        st.session_state.admin_id = admin_id
                        st.session_state.admin_role = role
                        st.session_state.user_name = username
                        
                        st.success(f"✅ {message} - Role: {role.upper()}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 2rem;
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            border-radius: 15px;
            border: 2px solid #3D4A47;'>
    <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem;'>
        🔒 Your data is secure with bank-level encryption
    </p>
    <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.85rem;'>
        Need help? Contact us at <span style='color: #C4935B;'>support@solivie.com</span>
    </p>
</div>
""", unsafe_allow_html=True)

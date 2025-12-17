"""
User Profile Page - Dark Luxury Theme
Enhanced with Reviews Integration
FIXED: All form elements styled properly + button styling
Tabs: Dashboard | Profile | My Bookings | My Reviews
"""
import streamlit as st
from backend.user.user_manager import UserManager
from backend.booking.booking_manager import BookingManager
from backend.payment.payment_processor import PaymentProcessor
from backend.payment.invoice_generator import InvoiceGenerator
from backend.user.review_manager import ReviewManager
from database.db_manager import get_db_session
from database.models import Room, User, Booking, Payment, Review
from utils.ui_components import SolivieUI
from utils.helpers import format_currency, format_datetime, get_star_rating_display
from utils.constants import BookingStatus
import config
import os


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="My Profile - Solivie Hotel",
    page_icon="👤",
    layout="wide"
)

# Apply dark luxury CSS
SolivieUI.inject_custom_css()

# CRITICAL: Enhanced form styling for ALL elements
st.markdown("""
<style>
/* ===== ALL INPUT FIELDS STYLING ===== */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select,
.stDateInput > div > div > input,
.stNumberInput > div > div > input {
    background-color: #2A3533 !important;
    color: #F5F5F0 !important;
    border: 2px solid #3D4A47 !important;
    border-radius: 10px !important;
    padding: 0.75rem !important;
    font-size: 1rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus,
.stDateInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #C4935B !important;
    box-shadow: 0 0 0 0.2rem rgba(196, 147, 91, 0.25) !important;
    background-color: #2C3E3A !important;
}

/* Disabled fields */
.stTextInput > div > div > input:disabled,
.stDateInput > div > div > input:disabled {
    background-color: #1F2524 !important;
    color: #9BA8A5 !important;
    border-color: #2A3533 !important;
    cursor: not-allowed !important;
    opacity: 0.7 !important;
}

/* Labels */
.stTextInput > label,
.stTextArea > label,
.stSelectbox > label,
.stDateInput > label,
.stNumberInput > label,
.stSlider > label {
    color: #C4935B !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    margin-bottom: 0.5rem !important;
}

/* Placeholder text */
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #7B8A87 !important;
    opacity: 0.7 !important;
}

/* Date input specific */
.stDateInput input[type="date"] {
    color: #F5F5F0 !important;
}

.stDateInput input[type="date"]::-webkit-calendar-picker-indicator {
    filter: invert(0.8);
    cursor: pointer;
}

/* Select dropdown */
.stSelectbox select option {
    background-color: #2A3533 !important;
    color: #F5F5F0 !important;
}

/* Slider styling */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #C4935B 0%, #D4A76A 100%) !important;
}

.stSlider > div > div > div > div > div {
    background-color: #C4935B !important;
}

/* ===== BUTTON STYLING - COMPREHENSIVE ===== */
/* Regular buttons outside forms */
.stButton > button,
div[data-testid="stButton"] > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.5px !important;
    transition: all 0.4s ease !important;
    text-transform: uppercase !important;
    font-size: 0.9rem !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
}

/* Primary buttons */
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

/* Secondary buttons */
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

/* ===== FORM SUBMIT BUTTONS - CRITICAL FIX ===== */
.stForm button[kind="primary"],
.stForm button[data-testid="stFormSubmitButton"],
button[data-testid="stFormSubmitButton"] {
    background: linear-gradient(135deg, #C4935B 0%, #B8875A 100%) !important;
    color: #1A1F1E !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.875rem 1.5rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 15px rgba(196, 147, 91, 0.3) !important;
    transition: all 0.4s ease !important;
    cursor: pointer !important;
    width: 100% !important;
}

.stForm button[kind="primary"]:hover,
.stForm button[data-testid="stFormSubmitButton"]:hover,
button[data-testid="stFormSubmitButton"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(196, 147, 91, 0.5) !important;
    background: linear-gradient(135deg, #D4A76A 0%, #C4935B 100%) !important;
}

.stForm button[kind="primary"]:active,
button[data-testid="stFormSubmitButton"]:active {
    transform: translateY(-1px) !important;
}

/* Secondary form buttons */
.stForm button[kind="secondary"] {
    background: transparent !important;
    color: #C4935B !important;
    border: 2px solid #C4935B !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

.stForm button[kind="secondary"]:hover {
    background: rgba(196, 147, 91, 0.1) !important;
    border-color: #D4A76A !important;
    color: #D4A76A !important;
}

/* Caption text */
.stCaption {
    color: #9BA8A5 !important;
    font-size: 0.875rem !important;
}

/* Checkbox styling */
.stCheckbox > label {
    color: #F5F5F0 !important;
}

.stCheckbox > div {
    background-color: #2A3533 !important;
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: #2A3533 !important;
    color: #C4935B !important;
    border: 2px solid #3D4A47 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

.streamlit-expanderHeader:hover {
    border-color: #C4935B !important;
    background-color: #2C3E3A !important;
}

/* Download button specific */
.stDownloadButton > button {
    background: linear-gradient(135deg, #C4935B 0%, #B8875A 100%) !important;
    color: #1A1F1E !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.75rem 1.5rem !important;
    text-transform: uppercase !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(196, 147, 91, 0.5) !important;
    background: linear-gradient(135deg, #D4A76A 0%, #C4935B 100%) !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# AUTHENTICATION CHECK
# ============================================================================

if not st.session_state.get('logged_in'):
    st.markdown("""
    <div style='background: linear-gradient(145deg, #3D2A2A 0%, #2C2020 100%);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                border: 2px solid #A95F5F;
                margin: 2rem 0;'>
        <h2 style='color: #D4A76A; margin: 0 0 1rem 0;'>🔐 Login Required</h2>
        <p style='color: #F5F5F0; font-size: 1.1rem; margin: 0;'>
            Please login to view your profile
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔐 LOGIN", use_container_width=True, type="primary", key="profile_login"):
            st.switch_page("pages/2_🔐_Login.py")
    with col2:
        if st.button("📝 REGISTER", use_container_width=True, type="secondary", key="profile_register"):
            st.switch_page("pages/3_📝_Register.py")
    with col3:
        if st.button("🏠 HOME", use_container_width=True, type="secondary", key="profile_home"):
            st.switch_page("app.py")
    st.stop()


# ============================================================================
# LOAD USER DATA
# ============================================================================

user = UserManager.get_user_profile(st.session_state.user_id)
if not user:
    st.error("❌ User profile not found")
    st.stop()

stats = UserManager.get_user_statistics(st.session_state.user_id)


# ============================================================================
# PAGE HEADER
# ============================================================================

SolivieUI.page_header(
    f"Welcome, {user['first_name']}!",
    "Manage your profile, bookings, and reviews",
    "👤"
)


# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👤 Profile", "📋 My Bookings", "⭐ My Reviews"])


# ============================================================================
# TAB 1: DASHBOARD
# ============================================================================

with tab1:
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 2rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            📊 Account Overview
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Booking Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #6B8E7E;'>
            <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>🟢 Active Bookings</p>
            <p style='color: #6B8E7E; margin: 0; font-size: 2.5rem; font-weight: 700;'>{stats['total_bookings']}</p>
            <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.8rem;'>Confirmed & Pending</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #7B9CA8;'>
            <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>✅ Completed</p>
            <p style='color: #7B9CA8; margin: 0; font-size: 2.5rem; font-weight: 700;'>{stats['completed_bookings']}</p>
            <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.8rem;'>Finished stays</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #3D2A2A 0%, #2C2020 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #A95F5F;'>
            <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>🔴 Cancelled</p>
            <p style='color: #D4A76A; margin: 0; font-size: 2.5rem; font-weight: 700;'>{stats['cancelled_bookings']}</p>
            <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.8rem;'>Cancelled bookings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #C4935B;'>
            <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>💰 Total Spent</p>
            <p style='color: #C4935B; margin: 0; font-size: 2rem; font-weight: 700;'>{format_currency(stats['total_spent'])}</p>
            <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.8rem;'>All-time spending</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Loyalty & Account Info
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 2rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            🎁 Loyalty & Membership
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                    padding: 2rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #C4935B;'>
            <p style='color: #C4935B; margin: 0 0 1rem 0; font-size: 1.5rem;'>🎁 Loyalty Points</p>
            <p style='color: #C4935B; margin: 0; font-size: 3rem; font-weight: 700;'>{stats['loyalty_points']}</p>
            <p style='color: #9BA8A5; margin: 1rem 0 0 0; font-size: 0.9rem;'>Earn points with every booking!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 2rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #7B9CA8;'>
            <p style='color: #7B9CA8; margin: 0 0 1rem 0; font-size: 1.5rem;'>📅 Member Since</p>
            <p style='color: #7B9CA8; margin: 0; font-size: 3rem; font-weight: 700;'>{stats['account_age_days']}</p>
            <p style='color: #9BA8A5; margin: 1rem 0 0 0; font-size: 0.9rem;'>days | Joined {user['created_at'].strftime('%B %Y')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Get review count
        with get_db_session() as session:
            review_count = session.query(Review).filter_by(user_id=st.session_state.user_id).count()
        
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 2rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #C4935B;'>
            <p style='color: #C4935B; margin: 0 0 1rem 0; font-size: 1.5rem;'>⭐ Reviews Written</p>
            <p style='color: #C4935B; margin: 0; font-size: 3rem; font-weight: 700;'>{review_count}</p>
            <p style='color: #9BA8A5; margin: 1rem 0 0 0; font-size: 0.9rem;'>Share your experiences!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 1.5rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            ⚡ Quick Actions
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 SEARCH ROOMS", use_container_width=True, type="primary", key="dash_search"):
            st.switch_page("pages/4_🔍_Search_Rooms.py")
    
    with col2:
        if st.button("📅 VIEW CALENDAR", use_container_width=True, type="secondary", key="dash_calendar"):
            st.switch_page("pages/7_📅_Availability_Calendar.py")
    
    with col3:
        if st.button("🛒 MY CART", use_container_width=True, type="secondary", key="dash_cart"):
            st.switch_page("pages/5_🛒_Shopping_Cart.py")


# ============================================================================
# TAB 2: PROFILE INFORMATION
# ============================================================================

with tab2:
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 2rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            👤 Edit Profile Information
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name *", value=user['first_name'], key="fname")
        
        with col2:
            last_name = st.text_input("Last Name *", value=user['last_name'], key="lname")
        
        st.text_input("Email Address", value=user['email'], disabled=True, key="email_display")
        st.caption("📧 Email cannot be changed. Contact support if needed.")
        
        phone = st.text_input("Phone Number", value=user['phone_number'] or "", key="phone_update", placeholder="+1 (555) 123-4567")
        
        address = st.text_area("Address", value=user['address'] or "", key="address_update", height=80, placeholder="Street address, apartment, suite, etc.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            city = st.text_input("City", value=user['city'] or "", key="city_update", placeholder="New York")
        
        with col2:
            country = st.text_input("Country", value=user['country'] or "", key="country_update", placeholder="United States")
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        if st.form_submit_button("💾 SAVE CHANGES", use_container_width=True, type="primary"):
            # Validation
            if not first_name or not last_name:
                st.error("❌ First name and last name are required")
            else:
                success, msg = UserManager.update_profile(
                    st.session_state.user_id,
                    first_name,
                    last_name,
                    phone,
                    address,
                    city,
                    country
                )
                
                if success:
                    st.success(f"✅ {msg}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
    
    # ===== IDENTIFICATION INFORMATION =====
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 1.5rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            🆔 Identification Information
        </h3>
        <p style='color: #9BA8A5; margin: 0.5rem 0 0 0;'>
            📋 This information is used for hotel check-in verification
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    has_id_info = user.get('national_id') or user.get('passport_number')
    
    if has_id_info:
        col1, col2 = st.columns(2)
        
        with col1:
            if user.get('national_id'):
                st.text_input(
                    "🆔 National ID Number",
                    value=user['national_id'],
                    disabled=True,
                    key="display_national_id"
                )
            elif user.get('passport_number'):
                st.text_input(
                    "🛂 Passport Number",
                    value=user['passport_number'],
                    disabled=True,
                    key="display_passport"
                )
            
            if user.get('nationality'):
                st.text_input(
                    "🌍 Nationality",
                    value=user['nationality'],
                    disabled=True,
                    key="display_nationality"
                )
        
        with col2:
            if user.get('date_of_birth'):
                st.date_input(
                    "📅 Date of Birth",
                    value=user['date_of_birth'],
                    disabled=True,
                    key="display_dob"
                )
            
            if user.get('id_expiry_date'):
                expiry_date = user['id_expiry_date']
                st.date_input(
                    "⏰ ID Expiry Date",
                    value=expiry_date,
                    disabled=True,
                    key="display_expiry"
                )
                
                # Expiry warning
                from datetime import date
                if expiry_date:
                    days_until_expiry = (expiry_date - date.today()).days
                    if days_until_expiry < 90:
                        if days_until_expiry < 0:
                            st.error("⚠️ Your ID has expired! Please update your documents.")
                        elif days_until_expiry < 30:
                            st.warning(f"⚠️ Your ID expires in {days_until_expiry} days!")
                        else:
                            st.info(f"ℹ️ Your ID expires in {days_until_expiry} days.")
        
        st.markdown("""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    border: 2px solid #7B9CA8;
                    margin-top: 1rem;'>
            <p style='color: #7B9CA8; margin: 0; font-weight: 600;'>
                🔒 Security Notice
            </p>
            <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; line-height: 1.6;'>
                ID information cannot be edited online. Please contact support at 
                <strong style='color: #C4935B;'>support@solivie.com</strong> to update identification details.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                    padding: 2rem;
                    border-radius: 12px;
                    border: 2px solid #C4935B;
                    text-align: center;'>
            <p style='color: #D4A76A; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;'>
                ⚠️ No ID information on file
            </p>
            <p style='color: #9BA8A5; margin: 0;'>
                You may be required to provide identification documents at check-in.
            </p>
            <p style='color: #9BA8A5; margin: 1rem 0 0 0;'>
                💡 Contact support to add your ID information to your profile for faster check-in.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# TAB 3: MY BOOKINGS
# ============================================================================

with tab3:
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 2rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            📋 My Booking History
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    bookings = BookingManager.get_user_bookings(st.session_state.user_id)
    
    if not bookings:
        st.markdown("""
        <div class='solivie-card' style='text-align: center; padding: 3rem 2rem;'>
            <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 2rem;'>
                📭 No Bookings Yet
            </h3>
            <p style='color: #9BA8A5; margin: 0 0 2rem 0; font-size: 1.1rem;'>
                Start your journey with us by booking your first stay
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔍 SEARCH ROOMS", use_container_width=True, type="primary", key="booking_search"):
                st.switch_page("pages/4_🔍_Search_Rooms.py")
    else:
        # Booking Summary
        active_count = len([b for b in bookings if b['booking_status'] in ['confirmed', 'pending']])
        completed_count = len([b for b in bookings if b['booking_status'] == 'completed'])
        cancelled_count = len([b for b in bookings if b['booking_status'] == 'cancelled'])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #6B8E7E;'>
                <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>🟢 Active</p>
                <p style='color: #6B8E7E; margin: 0; font-size: 2.5rem; font-weight: 700;'>{active_count}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #7B9CA8;'>
                <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>✅ Completed</p>
                <p style='color: #7B9CA8; margin: 0; font-size: 2.5rem; font-weight: 700;'>{completed_count}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #3D2A2A 0%, #2C2020 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #A95F5F;'>
                <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>🔴 Cancelled</p>
                <p style='color: #D4A76A; margin: 0; font-size: 2.5rem; font-weight: 700;'>{cancelled_count}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #C4935B;'>
                <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>📊 Total</p>
                <p style='color: #C4935B; margin: 0; font-size: 2.5rem; font-weight: 700;'>{len(bookings)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Display bookings
        for idx, booking in enumerate(bookings):
            with get_db_session() as session:
                room = session.query(Room).filter_by(room_id=booking['room_id']).first()
                room_info = f"Room {room.room_number} ({room.room_type})" if room else "N/A"
                
                # Get payment info
                payment = session.query(Payment).filter_by(booking_id=booking['booking_id']).first()
                has_payment = payment is not None
            
            # Status emoji and color
            status_map = {
                'confirmed': ('🟢', '#6B8E7E', 'CONFIRMED'),
                'pending': ('🟡', '#C4935B', 'PENDING'),
                'completed': ('✅', '#7B9CA8', 'COMPLETED'),
                'cancelled': ('🔴', '#A95F5F', 'CANCELLED')
            }
            status_emoji, status_color, status_text = status_map.get(booking['booking_status'], ('⚪', '#9BA8A5', 'UNKNOWN'))
            
            st.markdown(f"""
            <div class='solivie-card' style='margin-bottom: 1.5rem; border: 2px solid {status_color};'>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style='margin-bottom: 1rem;'>
                    <span style='background: {status_color}; color: #1A1F1E; padding: 0.5rem 1rem; 
                                 border-radius: 8px; font-weight: 700; font-size: 0.9rem;'>
                        {status_emoji} {status_text}
                    </span>
                </div>
                <h4 style='color: #C4935B; margin: 0 0 1rem 0;'>
                    {booking['booking_reference']}
                </h4>
                <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                    🏨 <strong>{room_info}</strong>
                </p>
                <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                    📅 <strong>Check-in:</strong> {format_datetime(booking['check_in_date'])}
                </p>
                <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                    📅 <strong>Check-out:</strong> {format_datetime(booking['check_out_date'])}
                </p>
                <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                    👥 <strong>Guests:</strong> {booking['num_guests']}
                </p>
                """, unsafe_allow_html=True)
                
                if booking.get('special_requests'):
                    st.markdown(f"""
                    <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                                padding: 1rem;
                                border-radius: 10px;
                                border: 2px solid #7B9CA8;
                                margin-top: 1rem;'>
                        <p style='color: #7B9CA8; margin: 0 0 0.5rem 0; font-weight: 600;'>💬 Special Requests:</p>
                        <p style='color: #9BA8A5; margin: 0;'>{booking['special_requests']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            text-align: center;
                            border: 2px solid #C4935B;
                            margin-bottom: 1rem;'>
                    <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>💰 Total Amount</p>
                    <p style='color: #C4935B; margin: 0; font-size: 1.8rem; font-weight: 700;'>
                        {format_currency(booking['total_amount'])}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Download Invoice (for paid bookings)
                if has_payment and booking['booking_status'] in ['confirmed', 'completed']:
                    if st.button(
                        "📄 INVOICE",
                        key=f"invoice_{booking['booking_id']}",
                        use_container_width=True,
                        type="secondary"
                    ):
                        with st.spinner("Generating invoice..."):
                            with get_db_session() as session:
                                booking_obj = session.query(Booking).filter_by(booking_id=booking['booking_id']).first()
                                payment_obj = session.query(Payment).filter_by(booking_id=booking['booking_id']).first()
                                user_obj = session.query(User).filter_by(user_id=st.session_state.user_id).first()
                                room_obj = session.query(Room).filter_by(room_id=booking['room_id']).first()
                                
                                if all([booking_obj, payment_obj, user_obj, room_obj]):
                                    invoice_dir = InvoiceGenerator.ensure_invoice_directory()
                                    filename = InvoiceGenerator.get_invoice_filename(booking['booking_reference'])
                                    filepath = os.path.join(invoice_dir, filename)
                                    
                                    success, result = InvoiceGenerator.generate_booking_invoice(
                                        booking_obj, payment_obj, user_obj, room_obj, filepath
                                    )
                                    
                                    if success:
                                        with open(filepath, 'rb') as f:
                                            pdf_data = f.read()
                                        
                                        st.download_button(
                                            label="💾 DOWNLOAD PDF",
                                            data=pdf_data,
                                            file_name=filename,
                                            mime="application/pdf",
                                            key=f"download_{booking['booking_id']}",
                                            use_container_width=True
                                        )
                                        st.success("✅ Invoice ready!")
                                    else:
                                        st.error(f"❌ {result}")
                                else:
                                    st.error("❌ Missing data")
                
                # Cancel button (for active bookings)
                if booking['booking_status'] in ['pending', 'confirmed']:
                    if st.button(
                        "❌ CANCEL",
                        key=f"cancel_{booking['booking_id']}",
                        use_container_width=True,
                        type="secondary"
                    ):
                        success, refund, msg = BookingManager.cancel_booking(booking['booking_id'])
                        if success:
                            st.success(f"✅ {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
            
            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# TAB 4: MY REVIEWS
# ============================================================================

with tab4:
    # Sub-tabs for Leave Review and View My Reviews
    review_tab1, review_tab2, review_tab3 = st.tabs(["📝 Leave Review", "⭐ My Reviews", "👀 All Reviews"])
    
    # ===== SUB-TAB 1: LEAVE REVIEW =====
    with review_tab1:
        st.markdown("""
        <div class='solivie-card' style='margin-bottom: 2rem;'>
            <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
                📝 Leave a Review
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Get completed bookings without reviews
        with get_db_session() as session:
            completed_bookings = session.query(Booking).filter(
                Booking.user_id == st.session_state.user_id,
                Booking.booking_status == BookingStatus.COMPLETED
            ).all()
            
            # Filter out bookings with existing reviews
            bookings_without_reviews = []
            for booking in completed_bookings:
                existing_review = session.query(Review).filter_by(
                    booking_id=booking.booking_id
                ).first()
                if not existing_review:
                    bookings_without_reviews.append(booking)
        
        if not bookings_without_reviews:
            st.markdown("""
            <div class='solivie-card' style='text-align: center; padding: 2rem;'>
                <h4 style='color: #C4935B; margin: 0 0 1rem 0;'>
                    📭 No Completed Bookings Available for Review
                </h4>
                <p style='color: #9BA8A5; margin: 0;'>
                    💡 Complete a stay to leave a review!
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.form("review_form"):
                # Booking selection
                booking_options = {}
                for b in bookings_without_reviews:
                    with get_db_session() as session:
                        room = session.query(Room).filter_by(room_id=b.room_id).first()
                    booking_options[f"Booking {b.booking_reference} - Room {room.room_number} ({room.room_type})"] = b.booking_id
                
                selected = st.selectbox("Select Completed Booking *", list(booking_options.keys()))
                booking_id = booking_options[selected]
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                # Rating
                st.markdown("""
                <div style='padding: 1rem 0;'>
                    <h4 style='color: #C4935B; margin: 0;'>⭐ Rate Your Experience</h4>
                </div>
                """, unsafe_allow_html=True)
                
                rating = st.slider("Rating", 1, 5, 5, help="1 = Poor, 5 = Excellent")
                st.markdown(f"<h3 style='color: #C4935B; text-align: center;'>{get_star_rating_display(rating)}</h3>", unsafe_allow_html=True)
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                # Review text
                st.markdown("""
                <div style='padding: 1rem 0;'>
                    <h4 style='color: #C4935B; margin: 0;'>💬 Your Review</h4>
                </div>
                """, unsafe_allow_html=True)
                
                comment = st.text_area(
                    "Share your experience",
                    placeholder="Tell us about your stay at Solivie Hotel...",
                    height=150,
                    help="Be detailed and honest!"
                )
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                # Submit button
                if st.form_submit_button("📮 SUBMIT REVIEW", use_container_width=True, type="primary"):
                    if not comment or len(comment.strip()) < 10:
                        st.error("❌ Please write a review (at least 10 characters)")
                    else:
                        # Get booking details
                        with get_db_session() as session:
                            booking = session.query(Booking).filter_by(booking_id=booking_id).first()
                        
                        success, message = ReviewManager.create_review(
                            st.session_state.user_id,
                            booking.room_id,
                            booking_id,
                            rating,
                            comment
                        )
                        
                        if success:
                            st.success(f"✅ {message}")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
    
    # ===== SUB-TAB 2: MY REVIEWS =====
    with review_tab2:
        st.markdown("""
        <div class='solivie-card' style='margin-bottom: 2rem;'>
            <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
                ⭐ My Review History
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Get user's reviews
        with get_db_session() as session:
            my_reviews = session.query(Review).filter_by(
                user_id=st.session_state.user_id
            ).order_by(Review.review_date.desc()).all()
        
        if not my_reviews:
            st.markdown("""
            <div class='solivie-card' style='text-align: center; padding: 2rem;'>
                <h4 style='color: #C4935B; margin: 0 0 1rem 0;'>
                    📭 You Haven't Written Any Reviews Yet
                </h4>
                <p style='color: #9BA8A5; margin: 0;'>
                    💡 Complete a stay and share your experience!
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #6B8E7E;
                        margin-bottom: 2rem;'>
                <p style='color: #6B8E7E; margin: 0; font-size: 1.2rem; font-weight: 600;'>
                    ✅ You have written <strong>{len(my_reviews)}</strong> review(s)
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display user's reviews
            for review in my_reviews:
                with get_db_session() as session:
                    room = session.query(Room).filter_by(room_id=review.room_id).first()
                    booking = session.query(Booking).filter_by(booking_id=review.booking_id).first()
                
                # Status badge
                if review.status == 'approved':
                    status_badge = "✅ Approved"
                    status_color = "#6B8E7E"
                elif review.status == 'pending':
                    status_badge = "🟡 Pending"
                    status_color = "#C4935B"
                else:
                    status_badge = "🔴 Rejected"
                    status_color = "#A95F5F"
                
                st.markdown(f"""
                <div class='solivie-card' style='margin-bottom: 1.5rem; border: 2px solid {status_color};'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                        <div>
                            <h4 style='color: #C4935B; margin: 0;'>🏨 Room {room.room_number} - {room.room_type}</h4>
                            <p style='color: #9BA8A5; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>
                                Booking: {booking.booking_reference}
                            </p>
                        </div>
                        <div>
                            <span style='background: {status_color}; color: #1A1F1E; padding: 0.5rem 1rem; 
                                         border-radius: 8px; font-weight: 700; font-size: 0.85rem;'>
                                {status_badge}
                            </span>
                        </div>
                    </div>
                    <div style='font-size: 1.5rem; margin-bottom: 1rem;'>
                        {get_star_rating_display(review.rating)}
                    </div>
                    <p style='color: #F5F5F0; margin: 1rem 0; line-height: 1.6;'>"{review.comment}"</p>
                    <p style='color: #9BA8A5; font-size: 0.85rem; margin: 0;'>
                        📅 {review.review_date.strftime('%B %d, %Y at %I:%M %p')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # ===== SUB-TAB 3: ALL REVIEWS =====
    with review_tab3:
        st.markdown("""
        <div class='solivie-card' style='margin-bottom: 2rem;'>
            <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
                👀 Guest Reviews
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            room_type_filter = st.selectbox(
                "Filter by Room Type",
                ["All"] + list(config.ROOM_TYPES.keys()),
                key="review_room_filter"
            )
        
        with col2:
            sort_by = st.selectbox(
                "Sort by",
                ["Newest First", "Highest Rating", "Lowest Rating"],
                key="review_sort"
            )
        
        # Get approved reviews
        with get_db_session() as session:
            query = session.query(Review).filter_by(status='approved')
            
            if room_type_filter != "All":
                query = query.join(Room).filter(Room.room_type == room_type_filter)
            
            if sort_by == "Newest First":
                query = query.order_by(Review.review_date.desc())
            elif sort_by == "Highest Rating":
                query = query.order_by(Review.rating.desc())
            elif sort_by == "Lowest Rating":
                query = query.order_by(Review.rating.asc())
            
            all_reviews = query.all()
        
        if not all_reviews:
            st.info("📭 No reviews available yet")
        else:
            # Overall rating
            avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #3D3528 0%, #2C2820 100%); 
                        padding: 2rem; border-radius: 15px; text-align: center; 
                        margin: 2rem 0; border: 3px solid #C4935B;'>
                <h2 style='margin: 0; color: #C4935B; font-size: 2rem;'>Overall Guest Rating</h2>
                <h1 style='color: #C4935B; font-size: 4rem; margin: 0.5rem 0;'>{avg_rating:.1f}/5.0</h1>
                <p style='font-size: 2rem; margin: 0.5rem 0;'>{get_star_rating_display(int(round(avg_rating)))}</p>
                <p style='color: #9BA8A5; font-size: 1.1rem; margin: 0;'>Based on {len(all_reviews)} review(s)</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
            
            # Display all reviews
            for review in all_reviews:
                with get_db_session() as session:
                    review_user = session.query(User).filter_by(user_id=review.user_id).first()
                    room = session.query(Room).filter_by(room_id=review.room_id).first()
                
                st.markdown(f"""
                <div class='solivie-card' style='margin-bottom: 1.5rem;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                        <div>
                            <h4 style='color: #C4935B; margin: 0;'>👤 {review_user.first_name} {review_user.last_name[0]}.</h4>
                            <p style='color: #9BA8A5; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>
                                Room {room.room_number} - {room.room_type}
                            </p>
                        </div>
                        <div style='font-size: 1.5rem;'>
                            {get_star_rating_display(review.rating)}
                        </div>
                    </div>
                    <p style='color: #F5F5F0; margin: 1rem 0; line-height: 1.6;'>"{review.comment}"</p>
                    <p style='color: #9BA8A5; font-size: 0.85rem; margin: 0;'>
                        📅 {review.review_date.strftime('%B %d, %Y')}
                    </p>
                </div>
                """, unsafe_allow_html=True)


# ============================================================================
# FOOTER - LOGOUT BUTTON
# ============================================================================

st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])

with col2:
    if st.button("🏠 HOME", use_container_width=True, type="secondary", key="footer_home"):
        st.switch_page("app.py")

with col3:
    if st.button("🚪 LOGOUT", use_container_width=True, type="secondary", key="footer_logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

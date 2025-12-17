"""
Solivie Hotel Reservation System - Dark Luxury Homepage
Professional horizontal hero card with logo
"""

import streamlit as st
from database.db_manager import DatabaseManager
from utils.ui_components import SolivieUI
from datetime import date, timedelta
import config
import os


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=config.APP_NAME,
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark luxury CSS
SolivieUI.inject_custom_css()


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

if 'db_initialized' not in st.session_state:
    with st.spinner('🔄 Initializing database...'):
        DatabaseManager.setup_database()
        st.session_state.db_initialized = True


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False


# ============================================================================
# MAIN PAGE
# ============================================================================

def main():
    """Dark luxury homepage with horizontal hero card."""
    
    # ===== HORIZONTAL HERO CARD WITH LOGO ON LEFT =====
    logo_paths = ["assets/logo.jpg", "assets/logo.png", "assets/Logo-6.jpg", "Logo-6.jpg"]
    logo_path = None
    
    for path in logo_paths:
        if os.path.exists(path):
            logo_path = path
            break
    
    # Professional horizontal card
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    col_logo, col_text = st.columns([1, 4])
    
    with col_logo:
        if logo_path:
            st.image(logo_path, width=180)
        else:
            st.markdown("""
            <div style='width: 180px; height: 180px; background: #2C3E3A; 
                        border-radius: 20px; display: flex; align-items: center; 
                        justify-content: center; border: 2px solid #C4935B;'>
                <span style='font-size: 3rem;'>🏨</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col_text:
        st.markdown("""
        <div style='padding: 1.5rem 0;'>
            <h1 style='color: #F5F5F0; font-size: 2.8rem; margin: 0 0 0.5rem 0; 
                       font-weight: 700; font-family: "Playfair Display", serif;'>
                Welcome to Solivie Hotel 
            </h1>
            <p style='color: #C4935B; font-size: 1.1rem; margin: 0; font-weight: 500;'>
                ✨ WHERE LUXURY MEETS COMFORT ✨
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ===== WELCOME MESSAGE =====
    if st.session_state.logged_in:
        st.success(f"👋 Welcome back, **{st.session_state.user_name}**! Ready to plan your next luxurious stay?")
    else:
        st.info("👋 **Discover Your Perfect Stay** - Login or register to unlock exclusive member benefits!")
    
    st.markdown("")
    
    # ===== QUICK SEARCH WIDGET =====
    st.markdown("### 🔍 Quick Room Search")
    st.markdown("<p style='color: #9BA8A5; margin-bottom: 1rem;'>Find your perfect room in seconds</p>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        
        with col1:
            check_in = st.date_input(
                "Check-in",
                value=date.today(),
                min_value=date.today(),
                key="home_checkin"
            )
        
        with col2:
            check_out = st.date_input(
                "Check-out",
                value=date.today() + timedelta(days=2),
                min_value=check_in + timedelta(days=1) if check_in else date.today() + timedelta(days=1),
                key="home_checkout"
            )
        
        with col3:
            guests = st.number_input(
                "Guests",
                min_value=1,
                max_value=10,
                value=2,
                key="home_guests"
            )
        
        with col4:
            st.markdown("")
            st.markdown("")
            if st.button("🔍 SEARCH", use_container_width=True, type="primary"):
                st.session_state.quick_search_checkin = check_in
                st.session_state.quick_search_checkout = check_out
                st.session_state.quick_search_guests = guests
                st.switch_page("pages/4_🔍_Search_Rooms.py")
    
    st.markdown("---")
    
    # ===== FEATURES SECTION =====
    st.markdown("### ✨ Why Choose Solivie Hotel?")
    st.markdown("<p style='color: #9BA8A5; margin-bottom: 2rem;'>Unparalleled service and amenities for the discerning traveler</p>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        SolivieUI.feature_card(
            "🔍",
            "Easy Booking",
            "Seamless reservation process with instant confirmation"
        )
    
    with col2:
        SolivieUI.feature_card(
            "💳",
            "Secure Payments",
            "Bank-level encryption for all transactions"
        )
    
    with col3:
        SolivieUI.feature_card(
            "⭐",
            "Best Prices",
            "Guaranteed lowest rates with exclusive member discounts"
        )
    
    with col4:
        SolivieUI.feature_card(
            "🎁",
            "Loyalty Rewards",
            "Earn points with every stay and enjoy VIP benefits"
        )
    
    st.markdown("---")
    
    # ===== ANIMATED STATISTICS (SYNCHRONIZED) =====
    st.markdown("### 📊 Trusted by Thousands")
    st.markdown("<p style='color: #9BA8A5; margin-bottom: 2rem;'>Join our growing community of satisfied guests</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='stats-container'>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        SolivieUI.stat_card("500+", "Happy Guests", "😊")
    
    with col2:
        SolivieUI.stat_card("50+", "Luxury Rooms", "🛏️")
    
    with col3:
        SolivieUI.stat_card("4.8★", "Average Rating", "⭐")
    
    with col4:
        SolivieUI.stat_card("24/7", "Concierge", "📞")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== ACTION BUTTONS =====
    if not st.session_state.logged_in:
        st.markdown("### 🚀 Get Started Today")
        st.markdown("<p style='color: #9BA8A5; margin-bottom: 1.5rem;'>Create your account for exclusive member benefits</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔐 LOGIN", use_container_width=True, type="primary"):
                st.switch_page("pages/2_🔐_Login.py")
        
        with col2:
            if st.button("📝 REGISTER", use_container_width=True, type="secondary"):
                st.switch_page("pages/3_📝_Register.py")
        
        with col3:
            if st.button("🔍 BROWSE ROOMS", use_container_width=True, type="secondary"):
                st.switch_page("pages/4_🔍_Search_Rooms.py")
    else:
        st.markdown("### 🎯 Quick Actions")
        st.markdown("<p style='color: #9BA8A5; margin-bottom: 1.5rem;'>Manage your reservations and explore available rooms</p>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔍 SEARCH ROOMS", use_container_width=True, type="primary"):
                st.switch_page("pages/4_🔍_Search_Rooms.py")
        
        with col2:
            if st.button("📋 MY BOOKINGS", use_container_width=True, type="secondary"):
                st.switch_page("pages/6_👤_My_Profile.py")
        
        with col3:
            if st.button("📅 CALENDAR", use_container_width=True, type="secondary"):
                st.switch_page("pages/15_📅_Availability_Calendar.py")
        
        with col4:
            if st.button("👤 PROFILE", use_container_width=True, type="secondary"):
                st.switch_page("pages/6_👤_My_Profile.py")
    
    st.markdown("---")
    
    # ===== ROOM TYPES (ANIMATED CARDS) =====
    st.markdown("### 🛏️ Our Premium Accommodations")
    st.markdown("<p style='color: #9BA8A5; margin-bottom: 2rem;'>Each room is meticulously designed for your ultimate comfort</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='rooms-container'>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    
    room_data = [
        ("Single", "🛏️", config.ROOM_TYPES.get("Single", {"base_price": 100, "capacity": 1})),
        ("Double", "🛏️🛏️", config.ROOM_TYPES.get("Double", {"base_price": 150, "capacity": 2})),
        ("Suite", "🏰", config.ROOM_TYPES.get("Suite", {"base_price": 250, "capacity": 4})),
        ("Deluxe", "👑", config.ROOM_TYPES.get("Deluxe", {"base_price": 350, "capacity": 4}))
    ]
    
    for col, (room_type, icon, details) in zip(cols, room_data):
        with col:
            st.markdown(f"""
            <div class='room-card'>
                <div class='room-icon'>{icon}</div>
                <h3 style='color: #F5F5F0; margin: 1rem 0; font-size: 1.5rem;
                          font-family: "Playfair Display", serif;'>{room_type}</h3>
                <p class='room-price'>
                    ${details['base_price']}
                </p>
                <p style='color: #9BA8A5; font-size: 0.9rem;'>/night</p>
                <hr style='border-color: #3D4A47; margin: 1rem 0;'>
                <p style='color: #9BA8A5; margin: 0.5rem 0;'>
                    👥 Up to {details['capacity']} guest(s)
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📋 VIEW ALL ROOMS & BOOK", use_container_width=True, type="primary"):
            st.switch_page("pages/4_🔍_Search_Rooms.py")
    
    st.markdown("---")
    
    # ===== AMENITIES =====
    st.markdown("### 🌟 World-Class Amenities")
    st.markdown("<p style='color: #9BA8A5; margin-bottom: 2rem;'>Everything you need for an unforgettable stay</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='solivie-card'>
            <h4 style='color: #C4935B; margin-top: 0;'>🏊 Recreation</h4>
            <ul style='color: #9BA8A5; line-height: 2;'>
                <li>Olympic Swimming Pool</li>
                <li>State-of-the-Art Fitness Center</li>
                <li>Luxury Spa & Wellness</li>
                <li>Entertainment Lounge</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='solivie-card'>
            <h4 style='color: #C4935B; margin-top: 0;'>🍽️ Dining Excellence</h4>
            <ul style='color: #9BA8A5; line-height: 2;'>
                <li>Award-Winning Restaurant</li>
                <li>24/7 Gourmet Room Service</li>
                <li>Premium Bar & Lounge</li>
                <li>Champagne Breakfast Buffet</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='solivie-card'>
            <h4 style='color: #C4935B; margin-top: 0;'>💼 Premium Services</h4>
            <ul style='color: #9BA8A5; line-height: 2;'>
                <li>High-Speed WiFi</li>
                <li>Valet Parking</li>
                <li>Personal Concierge</li>
                <li>Express Laundry Service</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== FOOTER =====
    SolivieUI.footer()


if __name__ == "__main__":
    main()

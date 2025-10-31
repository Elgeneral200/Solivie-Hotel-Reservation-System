"""
Hotel Reservation System - Main Application
Entry point for the Streamlit application.
"""

import streamlit as st
from database.db_manager import DatabaseManager
import config

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=config.APP_NAME,
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

if 'db_initialized' not in st.session_state:
    with st.spinner('Initializing database...'):
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
# CUSTOM CSS - DARK THEME
# ============================================================================

st.markdown("""
<style>
    /* Main container background */
    .main {
        background-color: #0e1117;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Feature boxes - DARK THEME */
    .feature-box {
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
    }
    
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.5);
        border-color: #7c3aed;
    }
    
    .feature-box h3 {
        font-size: 2.5rem;
        margin: 0 0 0.5rem 0;
    }
    
    .feature-box h4 {
        color: #e2e8f0;
        margin: 0.5rem 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .feature-box p {
        color: #94a3b8;
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
    }
    
    /* Room type boxes */
    .room-box {
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 2px solid #334155;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .room-box:hover {
        border-color: #7c3aed;
        transform: scale(1.05);
    }
    
    .room-box h3 {
        color: #e2e8f0;
        font-size: 1.5rem;
        margin: 0 0 0.5rem 0;
    }
    
    .room-box p {
        color: #94a3b8;
        margin: 0.3rem 0;
    }
    
    .room-box strong {
        color: #7c3aed;
        font-size: 1.3rem;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
    }
    
    /* Section headers */
    h3 {
        color: #e2e8f0 !important;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        border-top: 1px solid #334155;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN PAGE
# ============================================================================

def main():
    """Main application homepage."""
    
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>🏨 {config.APP_NAME}</h1>
        <p>Your Perfect Stay Awaits</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    if st.session_state.logged_in:
        st.success(f"👋 Welcome back, {st.session_state.user_name}!")
    else:
        st.info("👋 Welcome! Please login or register to make a booking.")
    
    # Features
    st.markdown("### ✨ Why Choose Us?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🔍</h3>
            <h4>Easy Search</h4>
            <p>Find rooms instantly</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>💳</h3>
            <h4>Secure Payment</h4>
            <p>Safe transactions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>⭐</h3>
            <h4>Best Prices</h4>
            <p>Great deals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-box">
            <h3>🎁</h3>
            <h4>Rewards</h4>
            <p>Loyalty points</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action buttons
    if not st.session_state.logged_in:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔐 Login", use_container_width=True, type="primary"):
                st.switch_page("pages/2_🔐_Login.py")
        with col2:
            if st.button("📝 Register", use_container_width=True):
                st.switch_page("pages/3_📝_Register.py")
        with col3:
            if st.button("🔍 Browse Rooms", use_container_width=True):
                st.switch_page("pages/4_🔍_Search_Rooms.py")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔍 Search Rooms", use_container_width=True, type="primary"):
                st.switch_page("pages/4_🔍_Search_Rooms.py")
        with col2:
            if st.button("📋 My Bookings", use_container_width=True):
                st.switch_page("pages/6_👤_My_Profile.py")
        with col3:
            if st.button("👤 Profile", use_container_width=True):
                st.switch_page("pages/6_👤_My_Profile.py")
    
    # Room types
    st.markdown("---")
    st.markdown("### 🛏️ Our Room Types")
    
    cols = st.columns(4)
    for col, (room_type, details) in zip(cols, config.ROOM_TYPES.items()):
        with col:
            st.markdown(f"""
            <div class="room-box">
                <h3>{room_type}</h3>
                <p><strong>${details['base_price']}/night</strong></p>
                <p>👥 {details['capacity']} guest(s)</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div class="footer">
        © 2025 {config.COMPANY_NAME} | Version {config.APP_VERSION}
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

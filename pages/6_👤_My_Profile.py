"""
User profile page
"""
import streamlit as st
from backend.user.user_manager import UserManager
from backend.booking.booking_manager import BookingManager
from database.db_manager import get_db_session
from database.models import Room
from utils.helpers import format_currency, format_datetime
import config

st.set_page_config(page_title="My Profile", page_icon="👤", layout="wide")

if not st.session_state.get('logged_in'):
    st.error("Please login")
    st.stop()

user = UserManager.get_user_profile(st.session_state.user_id)
if not user:
    st.error("User not found")
    st.stop()

stats = UserManager.get_user_statistics(st.session_state.user_id)

st.title(f"👤 Welcome, {user['first_name']}!")

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "👤 Profile", "📋 Bookings"])

# ===== TAB 1: DASHBOARD =====
with tab1:
    st.markdown("### 📊 Booking Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Bookings", stats['total_bookings'], "Confirmed & Pending")
    col2.metric("Completed", stats['completed_bookings'], "Finished stays")
    col3.metric("Cancelled", stats['cancelled_bookings'], "Cancelled bookings")
    col4.metric("Total Spent", format_currency(stats['total_spent']), "All bookings")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 Loyalty Points", stats['loyalty_points'])
    with col2:
        st.metric("📅 Account Age", f"{stats['account_age_days']} days")

# ===== TAB 2: PROFILE =====
with tab2:
    st.markdown("### 👤 Edit Profile")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", value=user['first_name'], key="fname")
        with col2:
            last_name = st.text_input("Last Name", value=user['last_name'], key="lname")
        
        st.text_input("Email", value=user['email'], disabled=True, key="email_display")
        phone = st.text_input("Phone", value=user['phone_number'] or "", key="phone_update")
        address = st.text_input("Address", value=user['address'] or "", key="address_update")
        
        col1, col2 = st.columns(2)
        with col1:
            city = st.text_input("City", value=user['city'] or "", key="city_update")
        with col2:
            country = st.text_input("Country", value=user['country'] or "", key="country_update")
        
        if st.form_submit_button("💾 Update Profile", use_container_width=True, type="primary"):
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
                st.success("✅ " + msg)
                st.rerun()
            else:
                st.error("❌ " + msg)

# ===== TAB 3: BOOKINGS =====
with tab3:
    st.markdown("### 📋 My Bookings")
    
    bookings = BookingManager.get_user_bookings(st.session_state.user_id)
    
    if not bookings:
        st.info("📭 No bookings yet")
    else:
        # ✅ Show booking summary
        st.markdown("**Summary:**")
        col1, col2, col3, col4 = st.columns(4)
        
        active_count = len([b for b in bookings if b['booking_status'] in ['confirmed', 'pending']])
        completed_count = len([b for b in bookings if b['booking_status'] == 'completed'])
        cancelled_count = len([b for b in bookings if b['booking_status'] == 'cancelled'])
        
        col1.metric("🟢 Active", active_count)
        col2.metric("✓ Completed", completed_count)
        col3.metric("🔴 Cancelled", cancelled_count)
        col4.metric("📊 Total", len(bookings))
        
        st.markdown("---")
        
        # ✅ Display all bookings
        st.markdown("**Booking Details:**")
        
        for idx, booking in enumerate(bookings):
            with get_db_session() as session:
                room = session.query(Room).filter_by(room_id=booking['room_id']).first()
                room_info = f"Room {room.room_number} ({room.room_type})" if room else "N/A"
            
            # Status badge color
            if booking['booking_status'] == 'confirmed':
                status_emoji = "🟢"
            elif booking['booking_status'] == 'pending':
                status_emoji = "🟡"
            elif booking['booking_status'] == 'completed':
                status_emoji = "✅"
            else:  # cancelled
                status_emoji = "🔴"
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                **{status_emoji} {booking['booking_reference']}** | {booking['booking_status'].upper()}
                
                🏨 **{room_info}**
                
                📅 Check-in: {format_datetime(booking['check_in_date'])}
                
                📅 Check-out: {format_datetime(booking['check_out_date'])}
                """)
            
            with col2:
                st.markdown(f"""
                **💰 Total**
                
                {format_currency(booking['total_amount'])}
                """)
                
                # ✅ Only show cancel button for active bookings
                if booking['booking_status'] in ['pending', 'confirmed']:
                    if st.button(
                        "❌ Cancel", 
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
            
            st.markdown("---")

# ===== LOGOUT BUTTON =====
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col3:
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

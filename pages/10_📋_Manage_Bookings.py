"""
Booking management page.
View and manage all bookings.
"""

import streamlit as st
from backend.booking.booking_manager import BookingManager
from database.db_manager import get_db_session
from database.models import Booking, Room, User
from utils.helpers import format_currency, format_datetime
from utils.constants import BookingStatus

st.set_page_config(page_title="Manage Bookings", page_icon="📋", layout="wide")

if not st.session_state.get('is_admin', False):
    st.error("❌ Admin access required")
    st.stop()

st.title("📋 Booking Management")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    status_filter = st.selectbox("Status", ["All"] + BookingStatus.get_all())
with col2:
    sort_order = st.selectbox("Sort", ["Newest First", "Oldest First", "Check-in Date"])
with col3:
    if st.button("🔄 Refresh"):
        st.rerun()

# Get bookings
with get_db_session() as session:
    query = session.query(Booking)
    if status_filter != "All":
        query = query.filter_by(booking_status=status_filter)
    
    if sort_order == "Newest First":
        query = query.order_by(Booking.created_at.desc())
    elif sort_order == "Oldest First":
        query = query.order_by(Booking.created_at.asc())
    else:
        query = query.order_by(Booking.check_in_date.asc())
    
    bookings = query.all()
    
    # ✅ FIX: Extract all data within the session
    bookings_data = []
    for booking in bookings:
        room = session.query(Room).filter_by(room_id=booking.room_id).first()
        user = session.query(User).filter_by(user_id=booking.user_id).first()
        
        bookings_data.append({
            'booking_id': booking.booking_id,
            'reference': booking.booking_reference,
            'status': booking.booking_status,
            'created_at': booking.created_at,
            'check_in': booking.check_in_date,
            'check_out': booking.check_out_date,
            'num_guests': booking.num_guests,
            'total_amount': booking.total_amount,
            'special_requests': booking.special_requests,
            'room_number': room.room_number if room else 'N/A',
            'room_type': room.room_type if room else 'N/A',
            'user_name': f"{user.first_name} {user.last_name}" if user else 'N/A',
            'user_email': user.email if user else 'N/A',
            'user_phone': user.phone_number if user else 'N/A'
        })

if not bookings_data:
    st.info("No bookings found")
else:
    st.success(f"Found {len(bookings_data)} booking(s)")
    
    for data in bookings_data:
        with st.expander(f"📋 {data['reference']} - {data['status'].upper()}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Booking Info**")
                st.write(f"Reference: {data['reference']}")
                st.write(f"Status: {data['status']}")
                st.write(f"Created: {format_datetime(data['created_at'])}")
            
            with col2:
                st.write("**Stay Details**")
                st.write(f"Room: {data['room_number']} ({data['room_type']})")
                st.write(f"Check-in: {format_datetime(data['check_in'])}")
                st.write(f"Check-out: {format_datetime(data['check_out'])}")
                st.write(f"Guests: {data['num_guests']}")
            
            with col3:
                st.write("**Customer**")
                st.write(f"Name: {data['user_name']}")
                st.write(f"Email: {data['user_email']}")
                st.write(f"Phone: {data['user_phone']}")
                st.write(f"**Total: {format_currency(data['total_amount'])}**")
            
            if data['special_requests']:
                st.write(f"**Special Requests:** {data['special_requests']}")
            
            # Actions
            if data['status'] in ['pending', 'confirmed']:
                if st.button("❌ Cancel", key=f"cancel_{data['booking_id']}"):
                    success, refund, msg = BookingManager.cancel_booking(data['booking_id'])
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

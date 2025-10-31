"""
User management page.
View and manage customer accounts.
"""

import streamlit as st
from database.db_manager import get_db_session
from database.models import User, Booking
from utils.helpers import format_currency

st.set_page_config(page_title="Manage Users", page_icon="👥", layout="wide")

if not st.session_state.get('is_admin', False):
    st.error("❌ Admin access required")
    st.stop()

st.title("👥 User Management")

# Search
search = st.text_input("🔍 Search by name or email")

# Get users
with get_db_session() as session:
    query = session.query(User)
    if search:
        query = query.filter(
            (User.first_name.contains(search)) |
            (User.last_name.contains(search)) |
            (User.email.contains(search))
        )
    users = query.all()
    
    # ✅ FIX: Extract all data within the session
    users_data = []
    for user in users:
        booking_count = session.query(Booking).filter_by(user_id=user.user_id).count()
        
        users_data.append({
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number or 'N/A',
            'address': user.address or 'N/A',
            'city': user.city or 'N/A',
            'country': user.country or 'N/A',
            'loyalty_points': user.loyalty_points,
            'account_status': user.account_status,
            'created_at': user.created_at,
            'booking_count': booking_count
        })

if not users_data:
    st.info("No users found")
else:
    st.success(f"Found {len(users_data)} user(s)")
    
    for data in users_data:
        with st.expander(f"👤 {data['first_name']} {data['last_name']} - {data['email']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Account Info**")
                st.write(f"Email: {data['email']}")
                st.write(f"Phone: {data['phone_number']}")
                st.write(f"Status: {data['account_status']}")
            
            with col2:
                st.write("**Location**")
                st.write(f"Address: {data['address']}")
                st.write(f"City: {data['city']}")
                st.write(f"Country: {data['country']}")
            
            with col3:
                st.write("**Activity**")
                st.write(f"Loyalty Points: {data['loyalty_points']}")
                st.write(f"Joined: {data['created_at'].strftime('%Y-%m-%d')}")
                st.write(f"Total Bookings: {data['booking_count']}")

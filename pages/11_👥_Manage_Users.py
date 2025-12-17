"""
User management page.
View and manage customer accounts.
UPDATED: Now displays ID information
"""

import streamlit as st
from database.db_manager import get_db_session
from database.models import User, Booking
from utils.helpers import format_currency
from datetime import date


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
    
    # Extract all data within the session
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
            # NEW: ID Information
            'national_id': user.national_id,
            'passport_number': user.passport_number,
            'nationality': user.nationality,
            'date_of_birth': user.date_of_birth,
            'id_expiry_date': user.id_expiry_date,
            # Original fields
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
        # Calculate ID expiry warning
        id_warning = ""
        if data['id_expiry_date']:
            days_until_expiry = (data['id_expiry_date'] - date.today()).days
            if days_until_expiry < 0:
                id_warning = " ⚠️ EXPIRED ID"
            elif days_until_expiry < 30:
                id_warning = f" ⚠️ ID Expires in {days_until_expiry} days"
        
        with st.expander(f"👤 {data['first_name']} {data['last_name']} - {data['email']}{id_warning}"):
            
            # Row 1: Account & Location
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**📧 Account Info**")
                st.write(f"Email: {data['email']}")
                st.write(f"Phone: {data['phone_number']}")
                st.write(f"Status: {data['account_status']}")
            
            with col2:
                st.markdown("**📍 Location**")
                st.write(f"Address: {data['address']}")
                st.write(f"City: {data['city']}")
                st.write(f"Country: {data['country']}")
            
            with col3:
                st.markdown("**📊 Activity**")
                st.write(f"Loyalty Points: {data['loyalty_points']}")
                st.write(f"Joined: {data['created_at'].strftime('%Y-%m-%d')}")
                st.write(f"Total Bookings: {data['booking_count']}")
            
            st.markdown("---")
            
            # Row 2: NEW - ID Information
            st.markdown("**🆔 Identification Information**")
            
            # Check if user has ID info
            has_id = data['national_id'] or data['passport_number']
            
            if has_id:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if data['national_id']:
                        st.write(f"**National ID:**")
                        st.write(f"{data['national_id']}")
                    elif data['passport_number']:
                        st.write(f"**Passport:**")
                        st.write(f"{data['passport_number']}")
                    else:
                        st.write("No ID")
                
                with col2:
                    st.write(f"**Nationality:**")
                    st.write(f"{data['nationality'] or 'N/A'}")
                
                with col3:
                    st.write(f"**Date of Birth:**")
                    if data['date_of_birth']:
                        st.write(f"{data['date_of_birth'].strftime('%Y-%m-%d')}")
                        age = (date.today() - data['date_of_birth']).days // 365
                        st.caption(f"Age: {age} years")
                    else:
                        st.write("N/A")
                
                with col4:
                    st.write(f"**ID Expiry:**")
                    if data['id_expiry_date']:
                        expiry_str = data['id_expiry_date'].strftime('%Y-%m-%d')
                        days_left = (data['id_expiry_date'] - date.today()).days
                        
                        if days_left < 0:
                            st.error(f"{expiry_str} (EXPIRED)")
                        elif days_left < 30:
                            st.warning(f"{expiry_str} ({days_left}d left)")
                        elif days_left < 90:
                            st.info(f"{expiry_str} ({days_left}d left)")
                        else:
                            st.write(f"{expiry_str}")
                    else:
                        st.write("N/A")
            else:
                st.warning("⚠️ No ID information on file - User may be required to show ID at check-in")

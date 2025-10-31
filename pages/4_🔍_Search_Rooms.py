"""
Room search page - FIXED VERSION
"""
import streamlit as st
from datetime import datetime, timedelta
from backend.booking.availability_checker import AvailabilityChecker
from backend.booking.pricing_calculator import PricingCalculator
from utils.helpers import format_currency, calculate_nights
import config

st.set_page_config(page_title="Search Rooms", page_icon="🔍", layout="wide")

if not st.session_state.get('logged_in'):
    st.error("Please login to search rooms")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login", use_container_width=True):
            st.switch_page("pages/2_🔐_Login.py")
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    st.stop()

st.title("🔍 Search Available Rooms")

# Initialize session state for search
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'search_nights' not in st.session_state:
    st.session_state.search_nights = 0

# Search form
st.markdown("### 🔎 Search Criteria")
col1, col2, col3, col4 = st.columns(4)

with col1:
    check_in = st.date_input("Check-in", value=datetime.now() + timedelta(days=1), key="checkin_date")

with col2:
    check_out = st.date_input("Check-out", value=datetime.now() + timedelta(days=4), key="checkout_date")

with col3:
    room_type = st.selectbox("Room Type", ["All"] + list(config.ROOM_TYPES.keys()), key="room_type_select")

with col4:
    num_guests = st.number_input("Guests", min_value=1, max_value=10, value=2, key="guests_number")

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    sort_by = st.selectbox("Sort by", ["Price: Low to High", "Price: High to Low"], key="sort_order")
with col2:
    search_btn = st.button("🔍 Search", key="search_button", use_container_width=True, type="primary")
with col3:
    pass

# Process search
if search_btn:
    check_in_dt = datetime.combine(check_in, datetime.min.time().replace(hour=14))
    check_out_dt = datetime.combine(check_out, datetime.min.time().replace(hour=11))
    
    if check_out_dt <= check_in_dt:
        st.error("❌ Check-out must be after check-in")
    else:
        nights = calculate_nights(check_in_dt, check_out_dt)
        room_type_filter = None if room_type == "All" else room_type
        
        with st.spinner("🔍 Searching for available rooms..."):
            rooms_data = AvailabilityChecker.get_available_rooms(
                check_in_dt, check_out_dt, room_type_filter, num_guests
            )
            
            if not rooms_data:
                st.warning("❌ No rooms available for selected dates")
            else:
                # Calculate prices
                for room in rooms_data:
                    total = PricingCalculator.calculate_total_price(
                        room['base_price'],
                        check_in_dt,
                        check_out_dt,
                        num_guests,
                        room['capacity']
                    )
                    room['total_price'] = total
                
                # Sort
                if sort_by == "Price: Low to High":
                    rooms_data.sort(key=lambda x: x['total_price'])
                else:
                    rooms_data.sort(key=lambda x: x['total_price'], reverse=True)
                
                # Store in session
                st.session_state.search_results = rooms_data
                st.session_state.search_nights = nights
                st.session_state.search_checkin = check_in_dt
                st.session_state.search_checkout = check_out_dt
                st.session_state.search_guests = num_guests

# Display results
if st.session_state.search_results:
    st.success(f"✅ Found {len(st.session_state.search_results)} room(s) for {st.session_state.search_nights} night(s)")
    st.markdown("---")
    
    for idx, room in enumerate(st.session_state.search_results):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            **🏨 Room {room['room_number']} - {room['room_type']}**
            - Capacity: {room['capacity']} guests
            - Floor: {room['floor_number']} | View: {room['view_type']}
            - {room['description']}
            """)
        
        with col2:
            st.metric("Per Night", format_currency(room['base_price']))
            st.metric("Total", format_currency(room['total_price']))
            
            if st.button(f"📅 Book Room {room['room_number']}", key=f"book_btn_{idx}_{room['room_id']}", use_container_width=True, type="primary"):
                st.session_state.booking_data = {
                    'room_id': room['room_id'],
                    'room_number': room['room_number'],
                    'room_type': room['room_type'],
                    'check_in': st.session_state.search_checkin,
                    'check_out': st.session_state.search_checkout,
                    'num_guests': st.session_state.search_guests,
                    'total_price': room['total_price'],
                    'nights': st.session_state.search_nights,
                    'base_price': room['base_price']
                }
                st.info("Redirecting to booking page...")
                st.switch_page("pages/5_📅_Book_Room.py")
        
        st.markdown("---")
else:
    st.info("ℹ️ Use the form above to search for rooms")

# Logout button
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col3:
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

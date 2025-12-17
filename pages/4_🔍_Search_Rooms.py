"""
Room search page - WITH ADVANCED FILTERS + SHOPPING CART
"""
import streamlit as st
from datetime import datetime, timedelta, date
from backend.booking.availability_checker import AvailabilityChecker
from backend.booking.pricing_calculator import PricingCalculator
from backend.booking.advanced_filters import AdvancedFilter
from backend.booking.cart_manager import CartManager
from utils.helpers import format_currency
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


# Initialize cart
CartManager.init_cart(st.session_state)


# ===== HEADER WITH CART BUTTON =====
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🔍 Search Available Rooms")
with col2:
    cart_count = CartManager.get_cart_count(st.session_state)
    if cart_count > 0:
        if st.button(f"🛒 Cart ({cart_count})", use_container_width=True, type="primary"):
            st.switch_page("pages/13_🛒_Shopping_Cart.py")
    else:
        st.button("🛒 Cart (0)", use_container_width=True, disabled=True)


# Initialize session state for search
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'search_nights' not in st.session_state:
    st.session_state.search_nights = 0


# Get filter options
filter_options = AdvancedFilter.get_filter_options()


# ===== BASIC SEARCH CRITERIA =====
st.markdown("### 🔎 Search Criteria")
col1, col2, col3, col4 = st.columns(4)


with col1:
    check_in = st.date_input(
        "Check-in", 
        value=date.today(),
        min_value=date.today(),
        key="checkin_date"
    )


with col2:
    min_checkout = check_in + timedelta(days=1) if check_in else date.today() + timedelta(days=1)
    default_checkout = check_in + timedelta(days=2) if check_in else date.today() + timedelta(days=2)
    
    check_out = st.date_input(
        "Check-out", 
        value=default_checkout,
        min_value=min_checkout,
        key="checkout_date"
    )


with col3:
    room_type = st.selectbox("Room Type", ["All"] + list(config.ROOM_TYPES.keys()), key="room_type_select")


with col4:
    num_guests = st.number_input("Guests", min_value=1, max_value=10, value=2, key="guests_number")


# Validate dates and show nights
if check_out <= check_in:
    st.error("❌ Check-out date must be after check-in date!")
else:
    nights_display = (check_out - check_in).days
    st.info(f"📅 Selected: **{nights_display} night(s)** from {check_in.strftime('%b %d')} to {check_out.strftime('%b %d, %Y')}")


# ===== ADVANCED FILTERS (COLLAPSIBLE) =====
st.markdown("---")
with st.expander("🔧 **Advanced Filters** (Optional)", expanded=False):
    st.markdown("#### 💰 Price Range")
    col1, col2 = st.columns(2)
    
    with col1:
        min_price = st.number_input(
            "Min Price (per night)", 
            min_value=0, 
            max_value=int(filter_options.get('max_price', 1000)),
            value=0,
            step=10,
            key="min_price_filter"
        )
    
    with col2:
        max_price = st.number_input(
            "Max Price (per night)", 
            min_value=0, 
            max_value=int(filter_options.get('max_price', 1000)),
            value=int(filter_options.get('max_price', 1000)),
            step=10,
            key="max_price_filter"
        )
    
    st.markdown("---")
    
    # Amenities filter
    st.markdown("#### ✨ Amenities")
    available_amenities = filter_options.get('amenities', [])
    
    if available_amenities:
        amenity_cols = st.columns(3)
        selected_amenities = []
        
        for idx, amenity in enumerate(available_amenities):
            col_idx = idx % 3
            with amenity_cols[col_idx]:
                if st.checkbox(amenity, key=f"amenity_{amenity}"):
                    selected_amenities.append(amenity)
    else:
        st.info("No amenity data available")
        selected_amenities = []
    
    st.markdown("---")
    
    # View and Floor filters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌅 View Type")
        available_views = filter_options.get('view_types', [])
        selected_views = st.multiselect(
            "Select view types",
            options=available_views,
            default=[],
            key="view_filter"
        )
    
    with col2:
        st.markdown("#### 🏢 Floor")
        available_floors = filter_options.get('floors', [])
        selected_floors = st.multiselect(
            "Select floors",
            options=available_floors,
            default=[],
            key="floor_filter"
        )


st.markdown("---")


# ===== SORT & SEARCH =====
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    sort_by = st.selectbox(
        "Sort by", 
        ["Price: Low to High", "Price: High to Low", "Room Number", "Capacity"],
        key="sort_order"
    )
with col2:
    search_btn = st.button("🔍 Search", key="search_button", use_container_width=True, type="primary")
with col3:
    pass


# ===== PROCESS SEARCH =====
if search_btn:
    check_in_dt = datetime.combine(check_in, datetime.min.time().replace(hour=14))
    check_out_dt = datetime.combine(check_out, datetime.min.time().replace(hour=11))
    
    if check_out <= check_in:
        st.error("❌ Check-out must be after check-in")
        st.stop()
    
    nights = (check_out - check_in).days
    
    if nights <= 0:
        st.error("❌ Invalid date range. Please select valid dates.")
        st.stop()
    
    if nights > 30:
        st.warning("⚠️ Bookings longer than 30 nights require approval. Please contact us.")
    
    room_type_list = None if room_type == "All" else [room_type]
    
    sort_map = {
        "Price: Low to High": "price_low",
        "Price: High to Low": "price_high",
        "Room Number": "room_number",
        "Capacity": "capacity"
    }
    
    with st.spinner("🔍 Searching for available rooms..."):
        rooms_data = AdvancedFilter.filter_rooms(
            check_in=check_in_dt,
            check_out=check_out_dt,
            min_price=min_price if min_price > 0 else None,
            max_price=max_price if max_price < filter_options.get('max_price', 1000) else None,
            room_types=room_type_list,
            amenities=selected_amenities if selected_amenities else None,
            floor_numbers=selected_floors if selected_floors else None,
            view_types=selected_views if selected_views else None,
            min_capacity=num_guests,
            sort_by=sort_map.get(sort_by, 'price_low')
        )
        
        if not rooms_data:
            st.warning("❌ No rooms available matching your criteria")
        else:
            for room in rooms_data:
                total = PricingCalculator.calculate_total_price(
                    room['base_price'],
                    check_in_dt,
                    check_out_dt,
                    num_guests,
                    room['capacity']
                )
                room['total_price'] = total
                room['nights'] = nights
            
            st.session_state.search_results = rooms_data
            st.session_state.search_nights = nights
            st.session_state.search_checkin = check_in_dt
            st.session_state.search_checkout = check_out_dt
            st.session_state.search_guests = num_guests


# ===== DISPLAY RESULTS =====
if st.session_state.search_results:
    st.success(f"✅ Found {len(st.session_state.search_results)} room(s) for {st.session_state.search_nights} night(s)")
    st.markdown("---")
    
    for idx, room in enumerate(st.session_state.search_results):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### 🏨 Room {room['room_number']} - {room['room_type']}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**👥 Capacity:** {room['capacity']} guests")
                st.write(f"**🏢 Floor:** {room['floor_number']}")
            with col_b:
                st.write(f"**🌅 View:** {room['view_type']}")
                st.write(f"**📊 Status:** {room['status']}")
            
            st.write(f"📝 {room['description']}")
            
            if room.get('amenities') and len(room['amenities']) > 0:
                st.markdown("**✨ Amenities:**")
                amenity_badges = " • ".join(room['amenities'])
                st.caption(amenity_badges)
        
        with col2:
            st.metric("💵 Per Night", format_currency(room['base_price']))
            st.metric(f"💰 Total ({st.session_state.search_nights} nights)", format_currency(room['total_price']))
            
            st.markdown("")
            
            # Check if already in cart
            in_cart = any(item['room_id'] == room['room_id'] for item in st.session_state.cart)
            
            # Two buttons: Add to Cart + Book Now
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                add_cart_btn = st.button(
                    "🛒 Add to Cart" if not in_cart else "✅ In Cart",
                    key=f"cart_btn_{idx}_{room['room_id']}",
                    use_container_width=True,
                    type="secondary",
                    disabled=in_cart
                )
                
                if add_cart_btn:
                    success, msg = CartManager.add_to_cart(
                        st.session_state,
                        room,
                        st.session_state.search_checkin,
                        st.session_state.search_checkout,
                        st.session_state.search_guests,
                        room['total_price'],
                        st.session_state.search_nights
                    )
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            
            with col_btn2:
                if st.button(
                    "📅 Book Now", 
                    key=f"book_btn_{idx}_{room['room_id']}", 
                    use_container_width=True, 
                    type="primary"
                ):
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
    st.info("ℹ️ Use the search form above to find available rooms")


# Logout button
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col3:
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

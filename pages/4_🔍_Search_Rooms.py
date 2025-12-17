"""
Room Search Page - Dark Luxury Theme
Simplified for Cart-Only Booking with Advanced Filters
"""
import streamlit as st
from datetime import datetime, timedelta, date
from backend.booking.availability_checker import AvailabilityChecker
from backend.booking.pricing_calculator import PricingCalculator
from backend.booking.advanced_filters import AdvancedFilter
from backend.booking.cart_manager import CartManager
from utils.ui_components import SolivieUI
from utils.helpers import format_currency
import config


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Search Rooms - Solivie Hotel",
    page_icon="🔍",
    layout="wide"
)

# Apply dark luxury CSS
SolivieUI.inject_custom_css()


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
            Please login to search and book rooms
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔐 LOGIN", use_container_width=True, type="primary"):
            st.switch_page("pages/2_🔐_Login.py")
    with col2:
        if st.button("📝 REGISTER", use_container_width=True, type="secondary"):
            st.switch_page("pages/3_📝_Register.py")
    with col3:
        if st.button("🏠 HOME", use_container_width=True, type="secondary"):
            st.switch_page("app.py")
    st.stop()


# ============================================================================
# INITIALIZE CART
# ============================================================================

CartManager.init_cart(st.session_state)


# ============================================================================
# HEADER WITH CART BUTTON
# ============================================================================

col1, col2 = st.columns([4, 1])

with col1:
    SolivieUI.page_header(
        "Search Available Rooms",
        "Find your perfect accommodation",
        "🔍"
    )

with col2:
    st.markdown("<div style='height: 5rem;'></div>", unsafe_allow_html=True)
    cart_count = CartManager.get_cart_count(st.session_state)
    if cart_count > 0:
        if st.button(f"🛒 CART ({cart_count})", use_container_width=True, type="primary", key="header_cart"):
            st.switch_page("pages/5_🛒_Shopping_Cart.py")
    else:
        st.markdown("""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 0.75rem;
                    border-radius: 10px;
                    text-align: center;
                    border: 2px solid #3D4A47;'>
            <span style='color: #9BA8A5; font-weight: 600;'>🛒 CART (0)</span>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'search_nights' not in st.session_state:
    st.session_state.search_nights = 0


# ============================================================================
# GET FILTER OPTIONS
# ============================================================================

filter_options = AdvancedFilter.get_filter_options()


# ============================================================================
# BASIC SEARCH CRITERIA
# ============================================================================

st.markdown("""
<div class='solivie-card' style='margin-bottom: 2rem;'>
    <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 1.5rem;'>
        🔎 Search Criteria
    </h3>
    <p style='color: #9BA8A5; margin: 0;'>
        Enter your travel dates and preferences
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    check_in = st.date_input(
        "Check-in Date",
        value=date.today(),
        min_value=date.today(),
        key="checkin_date"
    )

with col2:
    min_checkout = check_in + timedelta(days=1) if check_in else date.today() + timedelta(days=1)
    default_checkout = check_in + timedelta(days=2) if check_in else date.today() + timedelta(days=2)
    
    check_out = st.date_input(
        "Check-out Date",
        value=default_checkout,
        min_value=min_checkout,
        key="checkout_date"
    )

with col3:
    room_type = st.selectbox(
        "Room Type",
        ["All"] + list(config.ROOM_TYPES.keys()),
        key="room_type_select"
    )

with col4:
    num_guests = st.number_input(
        "Number of Guests",
        min_value=1,
        max_value=10,
        value=2,
        key="guests_number"
    )

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

# Validate dates and display nights
if check_out <= check_in:
    st.error("❌ Check-out date must be after check-in date!")
else:
    nights_display = (check_out - check_in).days
    st.markdown(f"""
    <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                border: 2px solid #7B9CA8;
                margin: 1rem 0;'>
        <p style='color: #7B9CA8; margin: 0; font-size: 1.1rem; font-weight: 600;'>
            📅 <strong>{nights_display} night(s)</strong> from {check_in.strftime('%b %d')} to {check_out.strftime('%b %d, %Y')}
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# ADVANCED FILTERS (COLLAPSIBLE)
# ============================================================================

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

with st.expander("🔧 **Advanced Filters** (Optional)", expanded=False):
    
    # Price Range
    st.markdown("""
    <div style='padding: 1rem 0;'>
        <h4 style='color: #C4935B; margin: 0 0 1rem 0;'>💰 Price Range (per night)</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        min_price = st.number_input(
            "Minimum Price",
            min_value=0,
            max_value=int(filter_options.get('max_price', 1000)),
            value=0,
            step=10,
            key="min_price_filter"
        )
    
    with col2:
        max_price = st.number_input(
            "Maximum Price",
            min_value=0,
            max_value=int(filter_options.get('max_price', 1000)),
            value=int(filter_options.get('max_price', 1000)),
            step=10,
            key="max_price_filter"
        )
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Amenities
    st.markdown("""
    <div style='padding: 1rem 0;'>
        <h4 style='color: #C4935B; margin: 0 0 1rem 0;'>✨ Amenities</h4>
    </div>
    """, unsafe_allow_html=True)
    
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
        st.info("ℹ️ No amenity filters available")
        selected_amenities = []
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # View and Floor
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='padding: 1rem 0;'>
            <h4 style='color: #C4935B; margin: 0 0 1rem 0;'>🌅 View Type</h4>
        </div>
        """, unsafe_allow_html=True)
        
        available_views = filter_options.get('view_types', [])
        selected_views = st.multiselect(
            "Select preferred views",
            options=available_views,
            default=[],
            key="view_filter"
        )
    
    with col2:
        st.markdown("""
        <div style='padding: 1rem 0;'>
            <h4 style='color: #C4935B; margin: 0 0 1rem 0;'>🏢 Floor Preference</h4>
        </div>
        """, unsafe_allow_html=True)
        
        available_floors = filter_options.get('floors', [])
        selected_floors = st.multiselect(
            "Select preferred floors",
            options=available_floors,
            default=[],
            key="floor_filter"
        )

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)


# ============================================================================
# SORT & SEARCH CONTROLS
# ============================================================================

col1, col2 = st.columns([3, 1])

with col1:
    sort_by = st.selectbox(
        "Sort Results By",
        ["Price: Low to High", "Price: High to Low", "Room Number", "Capacity"],
        key="sort_order"
    )

with col2:
    st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
    search_btn = st.button("🔍 SEARCH ROOMS", use_container_width=True, type="primary", key="search_button")

st.markdown("---")


# ============================================================================
# PROCESS SEARCH
# ============================================================================

if search_btn:
    # Convert dates to datetime
    check_in_dt = datetime.combine(check_in, datetime.min.time().replace(hour=14))
    check_out_dt = datetime.combine(check_out, datetime.min.time().replace(hour=11))
    
    # Validate dates
    if check_out <= check_in:
        st.error("❌ Check-out must be after check-in")
        st.stop()
    
    nights = (check_out - check_in).days
    
    if nights <= 0:
        st.error("❌ Invalid date range. Please select valid dates.")
        st.stop()
    
    if nights > 30:
        st.warning("⚠️ Bookings longer than 30 nights require approval. Please contact us.")
    
    # Prepare search parameters
    room_type_list = None if room_type == "All" else [room_type]
    
    sort_map = {
        "Price: Low to High": "price_low",
        "Price: High to Low": "price_high",
        "Room Number": "room_number",
        "Capacity": "capacity"
    }
    
    # Execute search
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
            # Calculate total prices for each room
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
            
            # Store results in session state
            st.session_state.search_results = rooms_data
            st.session_state.search_nights = nights
            st.session_state.search_checkin = check_in_dt
            st.session_state.search_checkout = check_out_dt
            st.session_state.search_guests = num_guests


# ============================================================================
# DISPLAY SEARCH RESULTS
# ============================================================================

if st.session_state.search_results:
    
    st.markdown(f"""
    <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                padding: 1.5rem;
                border-radius: 12px;
                text-align: center;
                border: 2px solid #6B8E7E;
                margin: 1.5rem 0;'>
        <h3 style='color: #6B8E7E; margin: 0;'>
            ✅ Found {len(st.session_state.search_results)} room(s) available for {st.session_state.search_nights} night(s)
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display each room
    for idx, room in enumerate(st.session_state.search_results):
        
        # Room Card
        st.markdown("""
        <div class='solivie-card' style='padding: 2rem; margin-bottom: 1.5rem;'>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        # Room Details Column
        with col1:
            st.markdown(f"""
            <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 1.8rem;'>
                🏨 Room {room['room_number']} - {room['room_type']}
            </h3>
            """, unsafe_allow_html=True)
            
            # Room Info
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                    <strong>👥 Capacity:</strong> {room['capacity']} guests
                </p>
                <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                    <strong>🏢 Floor:</strong> {room['floor_number']}
                </p>
                """, unsafe_allow_html=True)
            with col_b:
                st.markdown(f"""
                <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                    <strong>🌅 View:</strong> {room['view_type']}
                </p>
                <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                    <strong>📊 Status:</strong> <span style='color: #6B8E7E;'>{room['status']}</span>
                </p>
                """, unsafe_allow_html=True)
            
            # Description
            st.markdown(f"""
            <p style='color: #9BA8A5; margin: 1rem 0; line-height: 1.6;'>
                📝 {room['description']}
            </p>
            """, unsafe_allow_html=True)
            
            # Amenities
            if room.get('amenities') and len(room['amenities']) > 0:
                amenity_badges = " • ".join(room['amenities'])
                st.markdown(f"""
                <div style='margin-top: 1rem;'>
                    <p style='color: #C4935B; margin: 0 0 0.5rem 0; font-weight: 600;'>✨ Amenities:</p>
                    <p style='color: #9BA8A5; margin: 0;'>{amenity_badges}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Price & Action Column
        with col2:
            # Pricing cards
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        border: 2px solid #C4935B;
                        text-align: center;
                        margin-bottom: 1rem;'>
                <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>
                    💵 Price per Night
                </p>
                <p style='color: #C4935B; margin: 0; font-size: 2rem; font-weight: 700;'>
                    {format_currency(room['base_price'])}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        border: 2px solid #6B8E7E;
                        text-align: center;
                        margin-bottom: 1.5rem;'>
                <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>
                    💰 Total ({st.session_state.search_nights} nights)
                </p>
                <p style='color: #6B8E7E; margin: 0; font-size: 1.8rem; font-weight: 700;'>
                    {format_currency(room['total_price'])}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Check if room is already in cart
            in_cart = any(item['room_id'] == room['room_id'] for item in st.session_state.cart)
            
            # Add to Cart Button
            if in_cart:
                st.success("✅ In Cart")
                if st.button("🛒 VIEW CART", key=f"view_cart_{idx}_{room['room_id']}", use_container_width=True, type="primary"):
                    st.switch_page("pages/5_🛒_Shopping_Cart.py")
            else:
                if st.button(
                    "🛒 ADD TO CART",
                    key=f"add_cart_{idx}_{room['room_id']}",
                    use_container_width=True,
                    type="primary"
                ):
                    # Add room to cart
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
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(msg)
        
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # No search results yet
    st.markdown("""
    <div class='solivie-card' style='text-align: center; padding: 3rem 2rem;'>
        <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 2rem;'>
            🔍 Ready to Find Your Perfect Room?
        </h3>
        <p style='color: #9BA8A5; margin: 0 0 2rem 0; font-size: 1.1rem;'>
            Use the search form above to discover available accommodations
        </p>
        <div style='text-align: left; max-width: 600px; margin: 0 auto;'>
            <h4 style='color: #C4935B; margin: 0 0 1rem 0;'>💡 Search Tips:</h4>
            <ul style='color: #9BA8A5; line-height: 2;'>
                <li>Select your <strong>check-in</strong> and <strong>check-out</strong> dates</li>
                <li>Choose the <strong>number of guests</strong></li>
                <li>Use <strong>advanced filters</strong> for specific requirements</li>
                <li>Add multiple rooms to cart for group bookings</li>
                <li>All bookings are processed through the shopping cart</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if st.button("🏠 HOME", use_container_width=True, type="secondary", key="footer_home"):
        st.switch_page("app.py")

with col2:
    if st.button("👤 PROFILE", use_container_width=True, type="secondary", key="footer_profile"):
        st.switch_page("pages/6_👤_My_Profile.py")

with col3:
    if st.button("🚪 LOGOUT", use_container_width=True, type="secondary", key="footer_logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

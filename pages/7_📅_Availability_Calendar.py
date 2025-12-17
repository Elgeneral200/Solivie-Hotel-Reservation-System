"""
Room Availability Calendar - Dark Luxury Theme
Visual calendar showing room availability by month
Enhanced with modern design and better UX
"""
import streamlit as st
from backend.booking.availability_calendar import AvailabilityCalendar
from datetime import datetime, date, timedelta
import calendar
from utils.ui_components import SolivieUI


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Availability Calendar - Solivie Hotel",
    page_icon="📅",
    layout="wide"
)

# Apply dark luxury CSS
SolivieUI.inject_custom_css()

# Additional calendar-specific styling
st.markdown("""
<style>
/* ===== CALENDAR GRID STYLING ===== */
.calendar-day {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    border: 2px solid #3D4A47;
    border-radius: 10px;
    padding: 0.75rem;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
    min-height: 80px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.calendar-day:hover {
    border-color: #C4935B;
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(196, 147, 91, 0.3);
}

.calendar-day-header {
    background: linear-gradient(135deg, #C4935B 0%, #B8875A 100%);
    color: #1A1F1E;
    font-weight: 700;
    padding: 0.75rem;
    text-align: center;
    border-radius: 10px;
    margin-bottom: 0.5rem;
}

.calendar-month-nav {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 1.5rem;
    border-radius: 15px;
    border: 2px solid #C4935B;
    margin-bottom: 2rem;
}

.status-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
    margin: 0.25rem;
}

.status-available {
    background: rgba(107, 142, 126, 0.2);
    border: 2px solid #6B8E7E;
    color: #6B8E7E;
}

.status-booked {
    background: rgba(169, 95, 95, 0.2);
    border: 2px solid #A95F5F;
    color: #D4A76A;
}

.status-pending {
    background: rgba(196, 147, 91, 0.2);
    border: 2px solid #C4935B;
    color: #C4935B;
}

.status-past {
    background: rgba(155, 168, 165, 0.2);
    border: 2px solid #9BA8A5;
    color: #9BA8A5;
}

.room-availability-card {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 1.5rem;
    border-radius: 15px;
    border: 2px solid #3D4A47;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}

.room-availability-card:hover {
    border-color: #C4935B;
    box-shadow: 0 8px 25px rgba(196, 147, 91, 0.3);
    transform: translateY(-2px);
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
            Please login to view the availability calendar
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔐 LOGIN", use_container_width=True, type="primary", key="calendar_login"):
            st.switch_page("pages/2_🔐_Login.py")
    with col2:
        if st.button("📝 REGISTER", use_container_width=True, type="secondary", key="calendar_register"):
            st.switch_page("pages/3_📝_Register.py")
    with col3:
        if st.button("🏠 HOME", use_container_width=True, type="secondary", key="calendar_home"):
            st.switch_page("app.py")
    st.stop()


# ============================================================================
# PAGE HEADER
# ============================================================================

SolivieUI.page_header(
    "Availability Calendar",
    "View real-time room availability and plan your perfect stay",
    "📅"
)


# ============================================================================
# MONTH & ROOM TYPE SELECTOR
# ============================================================================

st.markdown("""
<div class='solivie-card' style='margin-bottom: 2rem;'>
    <h3 style='color: #C4935B; margin: 0 0 1.5rem 0; font-size: 1.5rem;'>
        🗓️ Select Month & Room Type
    </h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1, 1, 2, 1])

with col1:
    current_year = date.today().year
    year = st.selectbox(
        "📅 Year",
        range(current_year, current_year + 2),
        key="calendar_year"
    )

with col2:
    current_month = date.today().month
    month_names = list(calendar.month_name)[1:]
    month = st.selectbox(
        "📆 Month",
        range(1, 13),
        format_func=lambda x: month_names[x-1],
        index=current_month-1,
        key="calendar_month"
    )

with col3:
    room_type_filter = st.selectbox(
        "🏨 Filter by Room Type",
        ["All Rooms", "Single", "Double", "Suite", "Deluxe"],
        key="room_type_filter"
    )

with col4:
    st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
    if st.button("🔄 REFRESH", use_container_width=True, type="secondary", key="refresh_calendar"):
        st.rerun()


# ============================================================================
# LOAD CALENDAR DATA
# ============================================================================

room_type = None if room_type_filter == "All Rooms" else room_type_filter

with st.spinner("🔄 Loading calendar data..."):
    calendar_data = AvailabilityCalendar.get_month_availability(year, month, room_type)

if not calendar_data:
    st.error("❌ Failed to load calendar data")
    st.stop()


# ============================================================================
# LEGEND
# ============================================================================

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

st.markdown("""
<div class='solivie-card' style='margin-bottom: 2rem;'>
    <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 1.3rem;'>
        📊 Status Legend
    </h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='status-badge status-available'>
        🟢 AVAILABLE
    </div>
    <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Room is free to book</p>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='status-badge status-booked'>
        🔴 BOOKED
    </div>
    <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Room is confirmed</p>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='status-badge status-pending'>
        🟡 PENDING
    </div>
    <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Booking pending</p>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='status-badge status-past'>
        ⚫ PAST DATE
    </div>
    <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Date has passed</p>
    """, unsafe_allow_html=True)


# ============================================================================
# CALENDAR VIEW
# ============================================================================

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div class='solivie-card' style='margin-bottom: 1.5rem; text-align: center;'>
    <h2 style='color: #C4935B; margin: 0; font-size: 2.5rem;'>
        📅 {calendar.month_name[month]} {year}
    </h2>
</div>
""", unsafe_allow_html=True)

if not calendar_data['rooms']:
    st.markdown("""
    <div class='solivie-card' style='text-align: center; padding: 3rem 2rem;'>
        <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 2rem;'>
            🏨 No Rooms Found
        </h3>
        <p style='color: #9BA8A5; margin: 0; font-size: 1.1rem;'>
            No rooms match your selected filter. Try selecting "All Rooms"
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    dates = calendar_data['dates']
    rooms = calendar_data['rooms']
    total_rooms = len(rooms)
    
    # Summary stats
    st.markdown(f"""
    <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                padding: 1rem 2rem;
                border-radius: 12px;
                text-align: center;
                border: 2px solid #C4935B;
                margin-bottom: 2rem;'>
        <p style='color: #C4935B; margin: 0; font-size: 1.2rem; font-weight: 600;'>
            📊 Showing <strong>{total_rooms}</strong> Room(s)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Display each room's calendar
    for idx, room in enumerate(rooms):
        st.markdown(f"""
        <div class='room-availability-card'>
            <h3 style='color: #C4935B; margin: 0 0 1rem 0;'>
                🏨 Room {room['room_number']} - {room['room_type']}
            </h3>
        """, unsafe_allow_html=True)
        
        # Day names header
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        header_cols = st.columns(7)
        for day_idx, day_name in enumerate(day_names):
            header_cols[day_idx].markdown(
                f"<div class='calendar-day-header'>{day_name}</div>",
                unsafe_allow_html=True
            )
        
        # Get calendar data
        first_day = datetime(year, month, 1)
        first_weekday = first_day.weekday()
        daily_status = room['daily_status']
        num_days = len(dates)
        total_cells = first_weekday + num_days
        num_weeks = (total_cells + 6) // 7
        today = date.today()
        
        # Build calendar grid
        for week in range(num_weeks):
            week_cols = st.columns(7)
            
            for day_idx in range(7):
                cell_idx = week * 7 + day_idx
                
                # Empty cell before month starts
                if cell_idx < first_weekday:
                    week_cols[day_idx].markdown("")
                    continue
                
                # Calculate day number
                day_num = cell_idx - first_weekday + 1
                
                # Check if day is within month
                if day_num > num_days:
                    week_cols[day_idx].markdown("")
                    continue
                
                # Get date and status
                date_str = dates[day_num - 1]
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                status_info = daily_status.get(date_str, {'status': 'available', 'available': True})
                status = status_info['status']
                
                # Determine styling based on status
                if date_obj < today:
                    emoji = "⚫"
                    bg_color = "#3D4A47"
                    text_color = "#9BA8A5"
                    border_color = "#3D4A47"
                elif status == 'available':
                    emoji = "🟢"
                    bg_color = "rgba(107, 142, 126, 0.1)"
                    text_color = "#6B8E7E"
                    border_color = "#6B8E7E"
                elif status == 'booked':
                    emoji = "🔴"
                    bg_color = "rgba(169, 95, 95, 0.1)"
                    text_color = "#D4A76A"
                    border_color = "#A95F5F"
                else:  # pending
                    emoji = "🟡"
                    bg_color = "rgba(196, 147, 91, 0.1)"
                    text_color = "#C4935B"
                    border_color = "#C4935B"
                
                # Display day cell
                week_cols[day_idx].markdown(
                    f"""
                    <div style='background: {bg_color};
                                border: 2px solid {border_color};
                                border-radius: 10px;
                                padding: 0.75rem;
                                text-align: center;
                                transition: all 0.3s ease;
                                min-height: 80px;'>
                        <div style='font-weight: 700; font-size: 1.2rem; color: {text_color}; margin-bottom: 0.25rem;'>
                            {day_num}
                        </div>
                        <div style='font-size: 1.5rem;'>
                            {emoji}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)


# ============================================================================
# QUICK AVAILABILITY CHECK
# ============================================================================

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

st.markdown("""
<div class='solivie-card' style='margin-bottom: 2rem;'>
    <h3 style='color: #C4935B; margin: 0 0 1.5rem 0; font-size: 1.5rem;'>
        🔍 Quick Availability Check
    </h3>
    <p style='color: #9BA8A5; margin: 0;'>
        Check room availability for specific dates
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    check_start = st.date_input(
        "📅 Check-in Date",
        value=date.today(),
        min_value=date.today(),
        key="quick_check_in"
    )

with col2:
    check_end = st.date_input(
        "📅 Check-out Date",
        value=date.today() + timedelta(days=2),
        min_value=check_start + timedelta(days=1) if check_start else date.today() + timedelta(days=1),
        key="quick_check_out"
    )

with col3:
    st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
    check_button = st.button("🔍 CHECK", use_container_width=True, type="primary", key="check_avail_btn")

if check_button:
    if check_end <= check_start:
        st.error("❌ Check-out date must be after check-in date")
    else:
        with st.spinner("🔄 Checking availability..."):
            # Check availability for all rooms
            check_in_dt = datetime.combine(check_start, datetime.min.time())
            check_out_dt = datetime.combine(check_end, datetime.min.time())
            
            available_rooms = []
            booked_rooms = []
            
            for room in calendar_data['rooms']:
                available, conflicts = AvailabilityCalendar.get_room_availability_range(
                    room['room_id'],
                    check_in_dt,
                    check_out_dt
                )
                
                if available:
                    available_rooms.append(room)
                else:
                    booked_rooms.append((room, conflicts))
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            # Show results
            if available_rooms:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                            padding: 2rem;
                            border-radius: 15px;
                            border: 2px solid #6B8E7E;
                            text-align: center;
                            margin-bottom: 1.5rem;'>
                    <h3 style='color: #6B8E7E; margin: 0 0 1rem 0;'>
                        ✅ {len(available_rooms)} Room(s) Available!
                    </h3>
                    <p style='color: #9BA8A5; margin: 0;'>
                        From {check_start.strftime('%B %d, %Y')} to {check_end.strftime('%B %d, %Y')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show available rooms
                col1, col2 = st.columns(2)
                for idx, room in enumerate(available_rooms):
                    with col1 if idx % 2 == 0 else col2:
                        st.markdown(f"""
                        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                                    padding: 1.5rem;
                                    border-radius: 12px;
                                    border: 2px solid #6B8E7E;
                                    margin-bottom: 1rem;'>
                            <h4 style='color: #C4935B; margin: 0 0 0.5rem 0;'>
                                🏨 Room {room['room_number']}
                            </h4>
                            <p style='color: #9BA8A5; margin: 0;'>
                                {room['room_type']} • <span style='color: #6B8E7E;'>✅ Available</span>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("📅 BOOK NOW", use_container_width=True, type="primary", key="book_from_calendar"):
                        st.switch_page("pages/4_🔍_Search_Rooms.py")
            
            else:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #3D2A2A 0%, #2C2020 100%);
                            padding: 2rem;
                            border-radius: 15px;
                            border: 2px solid #A95F5F;
                            text-align: center;
                            margin-bottom: 1.5rem;'>
                    <h3 style='color: #D4A76A; margin: 0 0 1rem 0;'>
                        ❌ No Rooms Available
                    </h3>
                    <p style='color: #9BA8A5; margin: 0;'>
                        All rooms are booked for {check_start.strftime('%B %d, %Y')} to {check_end.strftime('%B %d, %Y')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show unavailable rooms
            if booked_rooms:
                st.markdown("---")
                st.markdown("""
                <h4 style='color: #D4A76A; margin: 1rem 0;'>
                    📋 Unavailable Rooms
                </h4>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                for idx, (room, conflicts) in enumerate(booked_rooms):
                    with col1 if idx % 2 == 0 else col2:
                        st.markdown(f"""
                        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                                    padding: 1.5rem;
                                    border-radius: 12px;
                                    border: 2px solid #A95F5F;
                                    margin-bottom: 1rem;'>
                            <h4 style='color: #C4935B; margin: 0 0 0.5rem 0;'>
                                🏨 Room {room['room_number']}
                            </h4>
                            <p style='color: #9BA8A5; margin: 0;'>
                                {room['room_type']} • <span style='color: #D4A76A;'>🔴 Booked</span>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)


# ============================================================================
# FOOTER NAVIGATION
# ============================================================================

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 HOME", use_container_width=True, type="secondary", key="footer_home"):
        st.switch_page("app.py")

with col2:
    if st.button("🔍 SEARCH ROOMS", use_container_width=True, type="secondary", key="footer_search"):
        st.switch_page("pages/4_🔍_Search_Rooms.py")

with col3:
    if st.button("👤 MY PROFILE", use_container_width=True, type="secondary", key="footer_profile"):
        st.switch_page("pages/6_👤_My_Profile.py")

with col4:
    if st.button("🚪 LOGOUT", use_container_width=True, type="secondary", key="footer_logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ============================================================================
# FOOTER
# ============================================================================

SolivieUI.footer()

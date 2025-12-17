"""
Room Availability Calendar
Visual calendar showing room availability by month
"""
import streamlit as st
from backend.booking.availability_calendar import AvailabilityCalendar
from datetime import datetime, date
import calendar
from datetime import timedelta


st.set_page_config(page_title="Availability Calendar", page_icon="📅", layout="wide")


if not st.session_state.get('logged_in'):
    st.error("❌ Please login to view calendar")
    st.stop()


st.title("📅 Room Availability Calendar")


# ===== MONTH SELECTOR =====
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    current_year = date.today().year
    year = st.selectbox("Year", range(current_year, current_year + 2), key="calendar_year")

with col2:
    current_month = date.today().month
    month_names = list(calendar.month_name)[1:]  # Skip empty first element
    month = st.selectbox("Month", range(1, 13), format_func=lambda x: month_names[x-1], index=current_month-1, key="calendar_month")

with col3:
    room_type_filter = st.selectbox(
        "Filter by Room Type",
        ["All Rooms", "Single", "Double", "Suite", "Deluxe"],
        key="room_type_filter"
    )


# Get availability data
room_type = None if room_type_filter == "All Rooms" else room_type_filter

with st.spinner("Loading calendar..."):
    calendar_data = AvailabilityCalendar.get_month_availability(year, month, room_type)


if not calendar_data:
    st.error("Failed to load calendar data")
    st.stop()


# ===== LEGEND =====
st.markdown("---")
st.markdown("### 📊 Legend")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("🟢 **Available** - Room is free")
with col2:
    st.markdown("🔴 **Booked** - Room is confirmed")
with col3:
    st.markdown("🟡 **Pending** - Booking pending")
with col4:
    st.markdown("⚫ **Past Date** - Date has passed")


st.markdown("---")


# ===== CALENDAR VIEW =====
st.markdown(f"### 📅 {calendar.month_name[month]} {year}")

if not calendar_data['rooms']:
    st.info("No rooms found for the selected filter")
else:
    # Get dates
    dates = calendar_data['dates']
    rooms = calendar_data['rooms']
    
    # Show summary
    total_rooms = len(rooms)
    st.caption(f"Showing {total_rooms} room(s)")
    
    st.markdown("---")
    
    # Display each room
    for room in rooms:
        with st.expander(f"🏨 Room {room['room_number']} ({room['room_type']})", expanded=True):
            
            # Create calendar grid (7 columns for days of week)
            st.markdown(f"**Room {room['room_number']}**")
            
            # Get day names
            day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            
            # Header row with day names
            header_cols = st.columns(7)
            for idx, day_name in enumerate(day_names):
                header_cols[idx].markdown(f"**{day_name}**")
            
            # Get first day of month (0=Monday, 6=Sunday)
            first_day = datetime(year, month, 1)
            first_weekday = first_day.weekday()
            
            # Build calendar grid
            daily_status = room['daily_status']
            day_counter = 1
            num_days = len(dates)
            
            # Calculate number of weeks needed
            total_cells = first_weekday + num_days
            num_weeks = (total_cells + 6) // 7
            
            today = date.today()
            
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
                    
                    # Get date string
                    date_str = dates[day_num - 1]
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                    
                    # Get status for this date
                    status_info = daily_status.get(date_str, {'status': 'available', 'available': True})
                    status = status_info['status']
                    
                    # Determine emoji and color
                    if date_obj < today:
                        emoji = "⚫"
                        color = "#999999"
                    elif status == 'available':
                        emoji = "🟢"
                        color = "#28a745"
                    elif status == 'booked':
                        emoji = "🔴"
                        color = "#dc3545"
                    else:  # pending
                        emoji = "🟡"
                        color = "#ffc107"
                    
                    # Display day
                    week_cols[day_idx].markdown(
                        f"<div style='text-align: center; padding: 5px;'>"
                        f"<div style='font-weight: bold;'>{day_num}</div>"
                        f"<div style='font-size: 20px;'>{emoji}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            
            st.markdown("---")


# ===== QUICK AVAILABILITY CHECK =====
st.markdown("---")
st.markdown("### 🔍 Quick Availability Check")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    check_start = st.date_input(
        "Check-in Date",
        value=date.today(),
        min_value=date.today(),
        key="quick_check_in"
    )

with col2:
    check_end = st.date_input(
        "Check-out Date",
        value=date.today() + timedelta(days=2),
        min_value=check_start + timedelta(days=1) if check_start else date.today() + timedelta(days=1),
        key="quick_check_out"
    )

with col3:
    st.markdown("")
    st.markdown("")
    if st.button("🔍 Check Availability", use_container_width=True, type="primary"):
        if check_end <= check_start:
            st.error("Check-out must be after check-in")
        else:
            # Check availability for all rooms
            from datetime import datetime as dt
            check_in_dt = dt.combine(check_start, dt.min.time())
            check_out_dt = dt.combine(check_end, dt.min.time())
            
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
            
            st.markdown("---")
            
            if available_rooms:
                st.success(f"✅ {len(available_rooms)} room(s) available!")
                
                for room in available_rooms:
                    st.markdown(f"🟢 **Room {room['room_number']}** ({room['room_type']}) - Available")
                
                if st.button("📅 Book Available Rooms", use_container_width=True):
                    st.switch_page("pages/2_🔍_Search_Rooms.py")
            else:
                st.warning("❌ No rooms available for selected dates")
            
            if booked_rooms:
                st.markdown("---")
                st.markdown("**Unavailable Rooms:**")
                for room, conflicts in booked_rooms:
                    st.markdown(f"🔴 **Room {room['room_number']}** ({room['room_type']}) - Booked")


# Logout
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col3:
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

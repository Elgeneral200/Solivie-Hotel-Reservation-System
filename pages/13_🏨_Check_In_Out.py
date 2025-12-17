"""
Check-in and Check-out management page for staff.
Handles guest arrivals, departures, and room status.
"""

import streamlit as st
from backend.booking.checkin_manager import CheckInManager
from utils.helpers import format_datetime
from datetime import datetime


st.set_page_config(page_title="Check-In/Out", page_icon="🏨", layout="wide")


# Check admin access
if not st.session_state.get('is_admin', False):
    st.error("❌ Admin access required")
    st.stop()


st.title("🏨 Check-In / Check-Out Management")


# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📥 Today's Arrivals", 
    "📤 Today's Departures", 
    "🏠 Current Occupancy",
    "🔍 Search Booking"
])


# ===== TAB 1: TODAY'S ARRIVALS =====
with tab1:
    st.markdown("### 📥 Expected Arrivals Today")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Arrivals", use_container_width=True):
            st.rerun()
    
    arrivals = CheckInManager.get_todays_arrivals()
    
    if not arrivals:
        st.info("✅ No arrivals expected today")
    else:
        # Summary
        checked_in_count = len([a for a in arrivals if a['checked_in']])
        pending_count = len(arrivals) - checked_in_count
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📋 Total Arrivals", len(arrivals))
        col2.metric("✅ Checked In", checked_in_count)
        col3.metric("⏳ Pending", pending_count)
        
        st.markdown("---")
        
        # Display each arrival
        for arrival in arrivals:
            # Color based on status
            if arrival['checked_in']:
                status_color = "🟢"
                status_text = "CHECKED IN"
            else:
                status_color = "🟡"
                status_text = "PENDING CHECK-IN"
            
            with st.expander(
                f"{status_color} {arrival['guest_name']} - Room {arrival['room_number']} ({arrival['room_type']}) - {status_text}",
                expanded=not arrival['checked_in']
            ):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**👤 Guest Information**")
                    st.write(f"**Name:** {arrival['guest_name']}")
                    st.write(f"**Email:** {arrival['guest_email']}")
                    st.write(f"**Phone:** {arrival['guest_phone']}")
                    st.write(f"**Guests:** {arrival['num_guests']}")
                
                with col2:
                    st.markdown("**🏨 Booking Details**")
                    st.write(f"**Reference:** {arrival['booking_reference']}")
                    st.write(f"**Room:** {arrival['room_number']} ({arrival['room_type']})")
                    st.write(f"**Check-in:** {format_datetime(arrival['check_in_date'])}")
                    st.write(f"**Check-out:** {format_datetime(arrival['check_out_date'])}")
                
                with col3:
                    st.markdown("**📋 Status**")
                    
                    # ID Verification status
                    if arrival['id_verified']:
                        st.success("✅ ID Verified")
                    else:
                        st.error("❌ ID Not Verified")
                        st.caption("⚠️ Verify ID before check-in")
                    
                    # Check-in status
                    if arrival['checked_in']:
                        st.success(f"✅ Checked in at {arrival['actual_check_in'].strftime('%H:%M')}")
                    else:
                        st.warning("⏳ Not checked in yet")
                
                # Special requests
                if arrival['special_requests']:
                    st.info(f"💬 **Special Requests:** {arrival['special_requests']}")
                
                st.markdown("---")
                
                # Actions
                if not arrival['checked_in']:
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    
                    with col_b:
                        if not arrival['id_verified']:
                            st.warning("⚠️ Verify ID first in Manage Bookings")
                    
                    with col_c:
                        check_in_btn = st.button(
                            "✅ CHECK IN",
                            key=f"checkin_{arrival['booking_id']}",
                            type="primary",
                            use_container_width=True,
                            disabled=not arrival['id_verified']
                        )
                        
                        if check_in_btn:
                            admin_id = st.session_state.get('admin_id')
                            success, msg = CheckInManager.check_in_guest(
                                arrival['booking_id'],
                                admin_id
                            )
                            if success:
                                st.success(f"✅ {msg}")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")


# ===== TAB 2: TODAY'S DEPARTURES =====
with tab2:
    st.markdown("### 📤 Expected Departures Today")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Departures", use_container_width=True):
            st.rerun()
    
    departures = CheckInManager.get_todays_departures()
    
    if not departures:
        st.info("✅ No departures expected today")
    else:
        # Summary
        checked_out_count = len([d for d in departures if d['checked_out']])
        pending_count = len(departures) - checked_out_count
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📋 Total Departures", len(departures))
        col2.metric("✅ Checked Out", checked_out_count)
        col3.metric("⏳ Pending", pending_count)
        
        st.markdown("---")
        
        # Display each departure
        for departure in departures:
            # Color based on status
            if departure['checked_out']:
                status_color = "✅"
                status_text = "CHECKED OUT"
            else:
                status_color = "🔴"
                status_text = "PENDING CHECK-OUT"
            
            with st.expander(
                f"{status_color} {departure['guest_name']} - Room {departure['room_number']} ({departure['room_type']}) - {status_text}",
                expanded=not departure['checked_out']
            ):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**👤 Guest Information**")
                    st.write(f"**Name:** {departure['guest_name']}")
                    st.write(f"**Email:** {departure['guest_email']}")
                    st.write(f"**Booking Ref:** {departure['booking_reference']}")
                
                with col2:
                    st.markdown("**🏨 Stay Details**")
                    st.write(f"**Room:** {departure['room_number']} ({departure['room_type']})")
                    st.write(f"**Checked in:** {format_datetime(departure['actual_check_in'])}")
                    st.write(f"**Expected checkout:** {format_datetime(departure['check_out_date'])}")
                    
                    if departure['checked_out']:
                        st.success(f"✅ Checked out at {departure['actual_check_out'].strftime('%H:%M')}")
                
                st.markdown("---")
                
                # Actions
                if not departure['checked_out']:
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_b:
                        check_out_btn = st.button(
                            "🚪 CHECK OUT",
                            key=f"checkout_{departure['booking_id']}",
                            type="primary",
                            use_container_width=True
                        )
                        
                        if check_out_btn:
                            admin_id = st.session_state.get('admin_id')
                            success, msg = CheckInManager.check_out_guest(
                                departure['booking_id'],
                                admin_id
                            )
                            if success:
                                st.success(f"✅ {msg}")
                                st.snow()
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")


# ===== TAB 3: CURRENT OCCUPANCY =====
with tab3:
    st.markdown("### 🏠 Currently Occupied Rooms")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Occupancy", use_container_width=True):
            st.rerun()
    
    occupied = CheckInManager.get_current_occupancy()
    
    if not occupied:
        st.info("🏨 All rooms are currently vacant")
    else:
        st.metric("🏠 Occupied Rooms", len(occupied))
        
        st.markdown("---")
        
        # Display occupied rooms
        for room in occupied:
            nights_stayed = (datetime.now().date() - room['check_in_date'].date()).days
            
            with st.expander(
                f"🏨 Room {room['room_number']} ({room['room_type']}) - {room['guest_name']}"
            ):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**👤 Guest**")
                    st.write(f"**Name:** {room['guest_name']}")
                    st.write(f"**Booking Ref:** {room['booking_reference']}")
                    st.write(f"**Number of Guests:** {room['num_guests']}")
                
                with col2:
                    st.markdown("**📅 Stay Duration**")
                    st.write(f"**Checked in:** {format_datetime(room['actual_check_in'])}")
                    st.write(f"**Expected checkout:** {format_datetime(room['check_out_date'])}")
                    st.write(f"**Nights stayed:** {nights_stayed}")


# ===== TAB 4: SEARCH BOOKING =====
with tab4:
    st.markdown("### 🔍 Search Booking")
    
    search_term = st.text_input(
        "Enter booking reference, guest name, or room number",
        placeholder="e.g., BK123ABC or John Doe or 101",
        key="search_booking"
    )
    
    if search_term:
        results = CheckInManager.search_booking(search_term)
        
        if not results:
            st.info("No bookings found matching your search")
        else:
            st.success(f"Found {len(results)} booking(s)")
            
            for result in results:
                status_icon = "🟢" if result['actual_check_in'] else "⏳"
                
                with st.expander(
                    f"{status_icon} {result['booking_reference']} - {result['guest_name']} - Room {result['room_number']}"
                ):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Booking Reference:** {result['booking_reference']}")
                        st.write(f"**Guest:** {result['guest_name']}")
                        st.write(f"**Room:** {result['room_number']}")
                    
                    with col2:
                        st.write(f"**Status:** {result['booking_status']}")
                        st.write(f"**Check-in:** {format_datetime(result['check_in_date'])}")
                        st.write(f"**Check-out:** {format_datetime(result['check_out_date'])}")
                    
                    st.markdown("---")
                    
                    # Status
                    if result['actual_check_in']:
                        st.success(f"✅ Checked in: {format_datetime(result['actual_check_in'])}")
                    else:
                        st.warning("⏳ Not checked in")
                    
                    if result['actual_check_out']:
                        st.info(f"🚪 Checked out: {format_datetime(result['actual_check_out'])}")
    else:
        st.info("💡 Enter a search term to find bookings")

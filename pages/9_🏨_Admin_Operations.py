"""
Admin Operations - Complete Booking & Check-In/Out Management
Merged: Manage Bookings + Check-In/Out functionality
Enhanced with Dark Luxury Theme
"""
import streamlit as st
from backend.booking.booking_manager import BookingManager
from backend.booking.checkin_manager import CheckInManager
from database.db_manager import get_db_session
from database.models import Booking, Room, User
from utils.ui_components import SolivieUI
from utils.helpers import format_currency, format_datetime
from utils.constants import BookingStatus
from datetime import datetime


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Admin Operations - Solivie Hotel",
    page_icon="🏨",
    layout="wide"
)

# Apply dark luxury CSS
SolivieUI.inject_custom_css()

# Additional operations-specific styling
st.markdown("""
<style>
/* ===== BOOKING CARDS ===== */
.booking-card {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 1.5rem;
    border-radius: 15px;
    border: 2px solid #3D4A47;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.booking-card:hover {
    border-color: #C4935B;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(196, 147, 91, 0.3);
}

/* ===== STATUS BADGES ===== */
.status-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-confirmed {
    background: rgba(107, 142, 126, 0.2);
    color: #6B8E7E;
    border: 2px solid #6B8E7E;
}

.status-pending {
    background: rgba(196, 147, 91, 0.2);
    color: #C4935B;
    border: 2px solid #C4935B;
}

.status-cancelled {
    background: rgba(169, 95, 95, 0.2);
    color: #D4A76A;
    border: 2px solid #A95F5F;
}

.status-completed {
    background: rgba(123, 156, 168, 0.2);
    color: #7B9CA8;
    border: 2px solid #7B9CA8;
}

/* ===== INFO SECTIONS ===== */
.info-section {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 1.25rem;
    border-radius: 12px;
    border: 2px solid #3D4A47;
    margin-bottom: 1rem;
}

.info-label {
    color: #9BA8A5;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.info-value {
    color: #F5F5F0;
    font-size: 1rem;
    font-weight: 600;
}

/* ===== VERIFICATION STATUS ===== */
.verification-verified {
    background: rgba(107, 142, 126, 0.2);
    border: 2px solid #6B8E7E;
    color: #6B8E7E;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    font-weight: 700;
}

.verification-not-verified {
    background: rgba(169, 95, 95, 0.2);
    border: 2px solid #A95F5F;
    color: #D4A76A;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    font-weight: 700;
}

/* ===== OCCUPANCY CARDS ===== */
.occupancy-card {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 1.5rem;
    border-radius: 15px;
    border: 2px solid #C4935B;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.occupancy-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(196, 147, 91, 0.4);
}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# ADMIN ACCESS CHECK
# ============================================================================

if not st.session_state.get('is_admin', False):
    st.markdown("""
    <div style='background: linear-gradient(145deg, #3D2A2A 0%, #2C2020 100%);
                padding: 3rem 2rem;
                border-radius: 15px;
                text-align: center;
                border: 2px solid #A95F5F;
                margin: 2rem 0;'>
        <h1 style='color: #D4A76A; margin: 0 0 1rem 0; font-size: 3rem;'>🔒</h1>
        <h2 style='color: #D4A76A; margin: 0 0 1rem 0;'>Admin Access Required</h2>
        <p style='color: #F5F5F0; font-size: 1.1rem; margin: 0;'>
            You need administrator privileges to access operations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 LOGIN AS ADMIN", use_container_width=True, type="primary", key="ops_login"):
            st.switch_page("pages/2_🔐_Login.py")
    with col2:
        if st.button("🏠 HOME", use_container_width=True, type="secondary", key="ops_home"):
            st.switch_page("app.py")
    st.stop()


# ============================================================================
# PAGE HEADER
# ============================================================================

SolivieUI.page_header(
    "Admin Operations Center",
    "Comprehensive booking management & guest check-in/out operations",
    "🏨"
)


# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2 = st.tabs(["📋 Manage Bookings", "🏨 Check-In / Check-Out"])


# ============================================================================
# TAB 1: MANAGE BOOKINGS
# ============================================================================

with tab1:
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 2rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            📋 Booking Management & ID Verification
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.selectbox(
            "🎯 Filter by Status",
            ["All"] + BookingStatus.get_all(),
            key="booking_status_filter"
        )
    
    with col2:
        sort_order = st.selectbox(
            "📊 Sort By",
            ["Newest First", "Oldest First", "Check-in Date"],
            key="booking_sort_order"
        )
    
    with col3:
        id_filter = st.selectbox(
            "🆔 ID Verification",
            ["All", "Verified", "Not Verified"],
            key="id_verification_filter"
        )
    
    with col4:
        st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
        if st.button("🔄 REFRESH", use_container_width=True, type="secondary", key="refresh_bookings"):
            st.rerun()
    
    # Get bookings
    with st.spinner("📊 Loading bookings..."):
        with get_db_session() as session:
            query = session.query(Booking)
            
            if status_filter != "All":
                query = query.filter_by(booking_status=status_filter)
            
            if id_filter == "Verified":
                query = query.filter_by(id_verified=True)
            elif id_filter == "Not Verified":
                query = query.filter_by(id_verified=False)
            
            if sort_order == "Newest First":
                query = query.order_by(Booking.created_at.desc())
            elif sort_order == "Oldest First":
                query = query.order_by(Booking.created_at.asc())
            else:
                query = query.order_by(Booking.check_in_date.asc())
            
            bookings = query.all()
            
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
                    'guest_id_number': booking.guest_id_number,
                    'id_verified': booking.id_verified,
                    'verification_date': booking.verification_date,
                    'room_number': room.room_number if room else 'N/A',
                    'room_type': room.room_type if room else 'N/A',
                    'user_name': f"{user.first_name} {user.last_name}" if user else 'N/A',
                    'user_email': user.email if user else 'N/A',
                    'user_phone': user.phone_number if user else 'N/A',
                    'user_national_id': user.national_id if user else None,
                    'user_passport': user.passport_number if user else None,
                    'user_nationality': user.nationality if user else 'N/A'
                })
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Display results
    if not bookings_data:
        st.markdown("""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 3rem 2rem;
                    border-radius: 15px;
                    text-align: center;
                    border: 2px solid #3D4A47;'>
            <h3 style='color: #C4935B; margin: 0 0 1rem 0;'>📭 No Bookings Found</h3>
            <p style='color: #9BA8A5; margin: 0;'>No bookings match your selected filters</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Summary metrics
        verified_count = len([b for b in bookings_data if b['id_verified']])
        not_verified_count = len(bookings_data) - verified_count
        active_count = len([b for b in bookings_data if b['status'] in ['confirmed', 'pending']])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #C4935B;'>
                <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem;'>📊 Total Bookings</p>
                <p style='color: #C4935B; margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;'>{len(bookings_data)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #6B8E7E;'>
                <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem;'>🟢 Active</p>
                <p style='color: #6B8E7E; margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;'>{active_count}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #6B8E7E;'>
                <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem;'>✅ ID Verified</p>
                <p style='color: #6B8E7E; margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;'>{verified_count}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #A95F5F;'>
                <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem;'>⚠️ Not Verified</p>
                <p style='color: #D4A76A; margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;'>{not_verified_count}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Display each booking
        for data in bookings_data:
            # Determine status badge
            if data['status'] == 'confirmed':
                status_class = 'status-confirmed'
                status_text = '✅ CONFIRMED'
            elif data['status'] == 'pending':
                status_class = 'status-pending'
                status_text = '⏳ PENDING'
            elif data['status'] == 'cancelled':
                status_class = 'status-cancelled'
                status_text = '❌ CANCELLED'
            else:
                status_class = 'status-completed'
                status_text = '✓ COMPLETED'
            
            # ID verification status
            if data['id_verified']:
                id_badge = "✅ ID Verified"
                id_color = "#6B8E7E"
            elif data['status'] in ['confirmed', 'pending']:
                id_badge = "⚠️ ID Not Verified"
                id_color = "#A95F5F"
            else:
                id_badge = ""
                id_color = "#3D4A47"
            
            with st.expander(
                f"📋 {data['reference']} - {status_text} {id_badge}",
                expanded=False
            ):
                # Booking Information
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class='info-section'>
                        <p style='color: #C4935B; margin: 0 0 1rem 0; font-weight: 700; font-size: 1.1rem;'>📋 Booking Info</p>
                    """, unsafe_allow_html=True)
                    st.write(f"**Reference:** {data['reference']}")
                    st.markdown(f"<span class='status-badge {status_class}'>{status_text}</span>", unsafe_allow_html=True)
                    st.write(f"**Created:** {format_datetime(data['created_at'])}")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class='info-section'>
                        <p style='color: #C4935B; margin: 0 0 1rem 0; font-weight: 700; font-size: 1.1rem;'>🏨 Stay Details</p>
                    """, unsafe_allow_html=True)
                    st.write(f"**Room:** {data['room_number']} ({data['room_type']})")
                    st.write(f"**Check-in:** {format_datetime(data['check_in'])}")
                    st.write(f"**Check-out:** {format_datetime(data['check_out'])}")
                    st.write(f"**Guests:** {data['num_guests']}")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class='info-section'>
                        <p style='color: #C4935B; margin: 0 0 1rem 0; font-weight: 700; font-size: 1.1rem;'>👤 Customer</p>
                    """, unsafe_allow_html=True)
                    st.write(f"**Name:** {data['user_name']}")
                    st.write(f"**Email:** {data['user_email']}")
                    st.write(f"**Phone:** {data['user_phone']}")
                    st.write(f"**Total:** {format_currency(data['total_amount'])}")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                # ID Verification Section
                st.markdown("""
                <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            border: 2px solid #C4935B;
                            margin-bottom: 1rem;'>
                    <h4 style='color: #C4935B; margin: 0 0 1rem 0;'>🆔 Guest Identification & Verification</h4>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.write("**ID on File:**")
                    if data['user_national_id']:
                        st.write(f"🆔 National ID: {data['user_national_id']}")
                    elif data['user_passport']:
                        st.write(f"🛂 Passport: {data['user_passport']}")
                    else:
                        st.warning("⚠️ No ID on file")
                
                with col2:
                    st.write("**Nationality:**")
                    st.write(data['user_nationality'])
                
                with col3:
                    st.write("**Verification Status:**")
                    if data['id_verified']:
                        st.success("✅ Verified")
                        if data['verification_date']:
                            st.caption(f"On: {data['verification_date'].strftime('%Y-%m-%d %H:%M')}")
                    else:
                        st.error("❌ Not Verified")
                
                with col4:
                    if not data['id_verified'] and data['status'] in ['confirmed', 'pending']:
                        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
                        if st.button(
                            "✅ VERIFY ID",
                            key=f"verify_{data['booking_id']}",
                            type="primary",
                            use_container_width=True
                        ):
                            with get_db_session() as session:
                                booking = session.query(Booking).filter_by(booking_id=data['booking_id']).first()
                                if booking:
                                    booking.id_verified = True
                                    booking.verification_date = datetime.now()
                                    if data['user_national_id']:
                                        booking.guest_id_number = data['user_national_id']
                                    elif data['user_passport']:
                                        booking.guest_id_number = data['user_passport']
                                    session.commit()
                                    st.success("✅ ID marked as verified!")
                                    st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Special Requests
                if data['special_requests']:
                    st.markdown(f"""
                    <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                                padding: 1.25rem;
                                border-radius: 10px;
                                border: 2px solid #7B9CA8;
                                margin-top: 1rem;'>
                        <p style='color: #7B9CA8; margin: 0 0 0.5rem 0; font-weight: 600;'>💬 Special Requests:</p>
                        <p style='color: #F5F5F0; margin: 0;'>{data['special_requests']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                # Actions
                if data['status'] in ['pending', 'confirmed']:
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    
                    with col_c:
                        if st.button(
                            "❌ CANCEL BOOKING",
                            key=f"cancel_{data['booking_id']}",
                            use_container_width=True,
                            type="secondary"
                        ):
                            success, refund, msg = BookingManager.cancel_booking(data['booking_id'])
                            if success:
                                st.success(f"✅ {msg}")
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")


# ============================================================================
# TAB 2: CHECK-IN / CHECK-OUT
# ============================================================================

with tab2:
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 2rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            🏨 Guest Check-In / Check-Out Operations
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sub-tabs
    checkin_tab1, checkin_tab2, checkin_tab3, checkin_tab4 = st.tabs([
        "📥 Today's Arrivals",
        "📤 Today's Departures",
        "🏠 Current Occupancy",
        "🔍 Search Booking"
    ])
    
    # ===== SUB-TAB 1: TODAY'S ARRIVALS =====
    with checkin_tab1:
        st.markdown("""
        <div class='solivie-card' style='margin-bottom: 1.5rem;'>
            <h4 style='color: #C4935B; margin: 0;'>📥 Expected Arrivals Today</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 REFRESH", use_container_width=True, type="secondary", key="refresh_arrivals"):
                st.rerun()
        
        with st.spinner("📥 Loading arrivals..."):
            arrivals = CheckInManager.get_todays_arrivals()
        
        if not arrivals:
            st.markdown("""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 2rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #6B8E7E;'>
                <p style='color: #6B8E7E; margin: 0; font-size: 1.2rem; font-weight: 600;'>
                    ✅ No arrivals expected today
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            checked_in_count = len([a for a in arrivals if a['checked_in']])
            pending_count = len(arrivals) - checked_in_count
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            text-align: center;
                            border: 2px solid #C4935B;'>
                    <p style='color: #9BA8A5; margin: 0;'>📋 Total</p>
                    <p style='color: #C4935B; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{len(arrivals)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            text-align: center;
                            border: 2px solid #6B8E7E;'>
                    <p style='color: #9BA8A5; margin: 0;'>✅ Checked In</p>
                    <p style='color: #6B8E7E; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{checked_in_count}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            text-align: center;
                            border: 2px solid #C4935B;'>
                    <p style='color: #9BA8A5; margin: 0;'>⏳ Pending</p>
                    <p style='color: #C4935B; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{pending_count}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
            
            # Display each arrival
            for arrival in arrivals:
                if arrival['checked_in']:
                    status_badge = "🟢 CHECKED IN"
                    border_color = "#6B8E7E"
                else:
                    status_badge = "🟡 PENDING CHECK-IN"
                    border_color = "#C4935B"
                
                with st.expander(
                    f"{status_badge} • {arrival['guest_name']} • Room {arrival['room_number']}",
                    expanded=not arrival['checked_in']
                ):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("""
                        <div class='info-section'>
                            <p style='color: #C4935B; margin: 0 0 1rem 0; font-weight: 700;'>👤 Guest Information</p>
                        """, unsafe_allow_html=True)
                        st.write(f"**Name:** {arrival['guest_name']}")
                        st.write(f"**Email:** {arrival['guest_email']}")
                        st.write(f"**Phone:** {arrival['guest_phone']}")
                        st.write(f"**Guests:** {arrival['num_guests']}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div class='info-section'>
                            <p style='color: #C4935B; margin: 0 0 1rem 0; font-weight: 700;'>🏨 Booking Details</p>
                        """, unsafe_allow_html=True)
                        st.write(f"**Reference:** {arrival['booking_reference']}")
                        st.write(f"**Room:** {arrival['room_number']} ({arrival['room_type']})")
                        st.write(f"**Check-in:** {format_datetime(arrival['check_in_date'])}")
                        st.write(f"**Check-out:** {format_datetime(arrival['check_out_date'])}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown("""
                        <div class='info-section'>
                            <p style='color: #C4935B; margin: 0 0 1rem 0; font-weight: 700;'>📋 Status</p>
                        """, unsafe_allow_html=True)
                        
                        if arrival['id_verified']:
                            st.success("✅ ID Verified")
                        else:
                            st.error("❌ ID Not Verified")
                            st.caption("⚠️ Verify in Manage Bookings")
                        
                        if arrival['checked_in']:
                            st.success(f"✅ Checked in at {arrival['actual_check_in'].strftime('%H:%M')}")
                        else:
                            st.warning("⏳ Not checked in")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    if arrival['special_requests']:
                        st.markdown(f"""
                        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                                    padding: 1rem;
                                    border-radius: 10px;
                                    border: 2px solid #7B9CA8;
                                    margin-top: 1rem;'>
                            <p style='color: #7B9CA8; margin: 0 0 0.5rem 0; font-weight: 600;'>💬 Special Requests:</p>
                            <p style='color: #F5F5F0; margin: 0;'>{arrival['special_requests']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                    
                    if not arrival['checked_in']:
                        col_a, col_b, col_c = st.columns([2, 1, 1])
                        
                        with col_b:
                            if not arrival['id_verified']:
                                st.warning("⚠️ ID verification required")
                        
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
    
    # ===== SUB-TAB 2: TODAY'S DEPARTURES =====
    with checkin_tab2:
        st.markdown("""
        <div class='solivie-card' style='margin-bottom: 1.5rem;'>
            <h4 style='color: #C4935B; margin: 0;'>📤 Expected Departures Today</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 REFRESH", use_container_width=True, type="secondary", key="refresh_departures"):
                st.rerun()
        
        with st.spinner("📤 Loading departures..."):
            departures = CheckInManager.get_todays_departures()
        
        if not departures:
            st.markdown("""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 2rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #6B8E7E;'>
                <p style='color: #6B8E7E; margin: 0; font-size: 1.2rem; font-weight: 600;'>
                    ✅ No departures expected today
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            checked_out_count = len([d for d in departures if d['checked_out']])
            pending_count = len(departures) - checked_out_count
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            text-align: center;
                            border: 2px solid #C4935B;'>
                    <p style='color: #9BA8A5; margin: 0;'>📋 Total</p>
                    <p style='color: #C4935B; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{len(departures)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            text-align: center;
                            border: 2px solid #6B8E7E;'>
                    <p style='color: #9BA8A5; margin: 0;'>✅ Checked Out</p>
                    <p style='color: #6B8E7E; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{checked_out_count}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            text-align: center;
                            border: 2px solid #C4935B;'>
                    <p style='color: #9BA8A5; margin: 0;'>⏳ Pending</p>
                    <p style='color: #C4935B; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{pending_count}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
            
            # Display each departure
            for departure in departures:
                if departure['checked_out']:
                    status_badge = "✅ CHECKED OUT"
                    border_color = "#6B8E7E"
                else:
                    status_badge = "🔴 PENDING CHECK-OUT"
                    border_color = "#A95F5F"
                
                with st.expander(
                    f"{status_badge} • {departure['guest_name']} • Room {departure['room_number']}",
                    expanded=not departure['checked_out']
                ):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("""
                        <div class='info-section'>
                            <p style='color: #C4935B; margin: 0 0 1rem 0; font-weight: 700;'>👤 Guest Information</p>
                        """, unsafe_allow_html=True)
                        st.write(f"**Name:** {departure['guest_name']}")
                        st.write(f"**Email:** {departure['guest_email']}")
                        st.write(f"**Reference:** {departure['booking_reference']}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div class='info-section'>
                            <p style='color: #C4935B; margin: 0 0 1rem 0; font-weight: 700;'>🏨 Stay Details</p>
                        """, unsafe_allow_html=True)
                        st.write(f"**Room:** {departure['room_number']} ({departure['room_type']})")
                        st.write(f"**Checked in:** {format_datetime(departure['actual_check_in'])}")
                        st.write(f"**Expected checkout:** {format_datetime(departure['check_out_date'])}")
                        
                        if departure['checked_out']:
                            st.success(f"✅ Checked out at {departure['actual_check_out'].strftime('%H:%M')}")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                    
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
    
    # ===== SUB-TAB 3: CURRENT OCCUPANCY =====
    with checkin_tab3:
        st.markdown("""
        <div class='solivie-card' style='margin-bottom: 1.5rem;'>
            <h4 style='color: #C4935B; margin: 0;'>🏠 Currently Occupied Rooms</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 REFRESH", use_container_width=True, type="secondary", key="refresh_occupancy"):
                st.rerun()
        
        with st.spinner("🏠 Loading occupancy..."):
            occupied = CheckInManager.get_current_occupancy()
        
        if not occupied:
            st.markdown("""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 2rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #6B8E7E;'>
                <p style='color: #6B8E7E; margin: 0; font-size: 1.2rem; font-weight: 600;'>
                    🏨 All rooms are currently vacant
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #C4935B;
                        margin-bottom: 2rem;'>
                <p style='color: #C4935B; margin: 0; font-size: 1.5rem; font-weight: 700;'>
                    🏠 {len(occupied)} Room(s) Occupied
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display occupied rooms
            col1, col2 = st.columns(2)
            for idx, room in enumerate(occupied):
                nights_stayed = (datetime.now().date() - room['check_in_date'].date()).days
                
                with col1 if idx % 2 == 0 else col2:
                    st.markdown(f"""
                    <div class='occupancy-card'>
                        <h4 style='color: #C4935B; margin: 0 0 1rem 0;'>
                            🏨 Room {room['room_number']} - {room['room_type']}
                        </h4>
                        <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                            <strong>👤 Guest:</strong> {room['guest_name']}
                        </p>
                        <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                            <strong>📋 Booking:</strong> {room['booking_reference']}
                        </p>
                        <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                            <strong>👥 Guests:</strong> {room['num_guests']}
                        </p>
                        <hr style='border-color: #3D4A47; margin: 1rem 0;'>
                        <p style='color: #9BA8A5; margin: 0.5rem 0; font-size: 0.9rem;'>
                            <strong>Check-in:</strong> {format_datetime(room['actual_check_in'])}
                        </p>
                        <p style='color: #9BA8A5; margin: 0.5rem 0; font-size: 0.9rem;'>
                            <strong>Expected checkout:</strong> {format_datetime(room['check_out_date'])}
                        </p>
                        <p style='color: #C4935B; margin: 0.5rem 0 0 0; font-weight: 700;'>
                            🌙 Nights stayed: {nights_stayed}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ===== SUB-TAB 4: SEARCH BOOKING =====
    with checkin_tab4:
        st.markdown("""
        <div class='solivie-card' style='margin-bottom: 1.5rem;'>
            <h4 style='color: #C4935B; margin: 0;'>🔍 Search Booking</h4>
        </div>
        """, unsafe_allow_html=True)
        
        search_term = st.text_input(
            "🔍 Enter booking reference, guest name, or room number",
            placeholder="e.g., BK123ABC or John Doe or 101",
            key="search_booking_term"
        )
        
        if search_term:
            with st.spinner("🔍 Searching..."):
                results = CheckInManager.search_booking(search_term)
            
            if not results:
                st.markdown("""
                <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                            padding: 2rem;
                            border-radius: 12px;
                            text-align: center;
                            border: 2px solid #3D4A47;'>
                    <p style='color: #9BA8A5; margin: 0; font-size: 1.1rem;'>
                        📭 No bookings found matching your search
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success(f"✅ Found {len(results)} booking(s)")
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                for result in results:
                    status_icon = "🟢" if result['actual_check_in'] else "⏳"
                    
                    with st.expander(
                        f"{status_icon} {result['booking_reference']} • {result['guest_name']} • Room {result['room_number']}"
                    ):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("""
                            <div class='info-section'>
                                <p style='color: #C4935B; margin: 0 0 1rem 0; font-weight: 700;'>📋 Booking Information</p>
                            """, unsafe_allow_html=True)
                            st.write(f"**Reference:** {result['booking_reference']}")
                            st.write(f"**Guest:** {result['guest_name']}")
                            st.write(f"**Room:** {result['room_number']}")
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown("""
                            <div class='info-section'>
                                <p style='color: #C4935B; margin: 0 0 1rem 0; font-weight: 700;'>📅 Dates</p>
                            """, unsafe_allow_html=True)
                            st.write(f"**Status:** {result['booking_status'].upper()}")
                            st.write(f"**Check-in:** {format_datetime(result['check_in_date'])}")
                            st.write(f"**Check-out:** {format_datetime(result['check_out_date'])}")
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                        
                        if result['actual_check_in']:
                            st.success(f"✅ Checked in: {format_datetime(result['actual_check_in'])}")
                        else:
                            st.warning("⏳ Not checked in")
                        
                        if result['actual_check_out']:
                            st.info(f"🚪 Checked out: {format_datetime(result['actual_check_out'])}")
        else:
            st.markdown("""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 2rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #3D4A47;'>
                <p style='color: #9BA8A5; margin: 0; font-size: 1.1rem;'>
                    💡 Enter a search term to find bookings
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
    if st.button("📊 DASHBOARD", use_container_width=True, type="secondary", key="footer_dashboard"):
        st.switch_page("pages/8_📊_Dashboard.py")

with col3:
    if st.button("⚙️ MANAGEMENT", use_container_width=True, type="secondary", key="footer_mgmt"):
        st.switch_page("pages/10_⚙️_Admin_Management.py")

with col4:
    if st.button("🚪 LOGOUT", use_container_width=True, type="secondary", key="footer_logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ============================================================================
# FOOTER
# ============================================================================

SolivieUI.footer()

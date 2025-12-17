"""
Admin Dashboard - Dark Luxury Theme
Displays key metrics, statistics, and system overview
Enhanced with professional styling and better UX
"""
import streamlit as st
from datetime import datetime, timedelta
from database.db_manager import get_db_session
from database.models import Booking, Room, User, Payment
from backend.booking.availability_checker import AvailabilityChecker
from utils.ui_components import SolivieUI
from utils.helpers import format_currency, get_percentage
import config


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Admin Dashboard - Solivie Hotel",
    page_icon="📊",
    layout="wide"
)

# Apply dark luxury CSS
SolivieUI.inject_custom_css()

# Additional dashboard-specific styling
st.markdown("""
<style>
/* ===== METRIC CARDS ===== */
.metric-card {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 1.5rem;
    border-radius: 15px;
    border: 2px solid #3D4A47;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.metric-card:hover {
    border-color: #C4935B;
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(196, 147, 91, 0.3);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #C4935B 0%, #D4A76A 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.5rem 0;
}

.metric-label {
    color: #9BA8A5;
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-subtitle {
    color: #7B9CA8;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

/* ===== STATUS BADGES ===== */
.status-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.85rem;
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

/* ===== BOOKING ROW ===== */
.booking-row {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 1rem 1.5rem;
    border-radius: 12px;
    border: 2px solid #3D4A47;
    margin-bottom: 0.75rem;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.booking-row:hover {
    border-color: #C4935B;
    transform: translateX(5px);
    box-shadow: 0 4px 15px rgba(196, 147, 91, 0.2);
}

/* ===== QUICK ACTION CARDS ===== */
.quick-action-card {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 2rem;
    border-radius: 15px;
    border: 2px solid #3D4A47;
    text-align: center;
    transition: all 0.4s ease;
    cursor: pointer;
    height: 100%;
}

.quick-action-card:hover {
    border-color: #C4935B;
    transform: translateY(-10px);
    box-shadow: 0 15px 40px rgba(196, 147, 91, 0.3);
}

.quick-action-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# AUTHENTICATION CHECK
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
            You need administrator privileges to access this page
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🏠 GO HOME", use_container_width=True, type="primary", key="admin_home"):
            st.switch_page("app.py")
    st.stop()


# ============================================================================
# PAGE HEADER
# ============================================================================

# Welcome message with admin badge
st.markdown(f"""
<div style='background: linear-gradient(135deg, #2C3E3A 0%, #5A726F 50%, #2C3E3A 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            border: 2px solid #C4935B;'>
    <div style='display: flex; align-items: center; justify-content: space-between;'>
        <div>
            <h1 style='color: #F5F5F0; margin: 0; font-size: 2.5rem;'>
                📊 Admin Dashboard
            </h1>
            <p style='color: #C4935B; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>
                Welcome back, <strong>{st.session_state.user_name}</strong>
            </p>
        </div>
        <div style='background: linear-gradient(135deg, #C4935B 0%, #B8875A 100%);
                    padding: 0.75rem 1.5rem;
                    border-radius: 10px;
                    color: #1A1F1E;
                    font-weight: 700;
                    font-size: 1rem;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;'>
            👑 {st.session_state.admin_role.upper()}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# PERIOD SELECTOR & REFRESH
# ============================================================================

st.markdown("""
<div class='solivie-card' style='margin-bottom: 2rem;'>
    <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 1.3rem;'>
        📅 Select Period
    </h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    date_range = st.selectbox(
        "Time Period",
        ["Today", "Last 7 Days", "Last 30 Days", "This Month"],
        key="dashboard_period"
    )

with col2:
    st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
    if st.button("🔄 REFRESH", use_container_width=True, type="secondary", key="refresh_dashboard"):
        st.rerun()

with col3:
    st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
    current_time = datetime.now().strftime("%I:%M %p")
    st.markdown(f"""
    <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                padding: 0.75rem;
                border-radius: 10px;
                text-align: center;
                border: 2px solid #3D4A47;'>
        <p style='color: #C4935B; margin: 0; font-weight: 600;'>🕐 {current_time}</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# CALCULATE DATE RANGE
# ============================================================================

today = datetime.now()
if date_range == "Today":
    start_date = today.replace(hour=0, minute=0, second=0)
elif date_range == "Last 7 Days":
    start_date = today - timedelta(days=7)
elif date_range == "Last 30 Days":
    start_date = today - timedelta(days=30)
else:
    start_date = today.replace(day=1, hour=0, minute=0, second=0)


# ============================================================================
# FETCH STATISTICS
# ============================================================================

with st.spinner("📊 Loading dashboard data..."):
    with get_db_session() as session:
        # Revenue & Payments
        payments = session.query(Payment).filter(
            Payment.payment_status == 'completed',
            Payment.payment_date >= start_date
        ).all()
        total_revenue = sum(p.amount for p in payments)
        num_transactions = len(payments)
        
        # Bookings
        bookings = session.query(Booking).filter(Booking.created_at >= start_date).all()
        total_bookings = len(bookings)
        confirmed_bookings = len([b for b in bookings if b.booking_status == 'confirmed'])
        
        # Rooms
        total_rooms = session.query(Room).count()
        available_rooms = session.query(Room).filter_by(status='available').count()
        occupied_rooms = session.query(Room).filter_by(status='occupied').count()
        maintenance_rooms = session.query(Room).filter_by(status='maintenance').count()
        cleaning_rooms = session.query(Room).filter_by(status='cleaning').count()
        
        # Users
        total_users = session.query(User).count()
        new_users = session.query(User).filter(User.created_at >= start_date).count()
        
        # Booking Status
        pending_bookings = session.query(Booking).filter_by(booking_status='pending').count()
        confirmed_total = session.query(Booking).filter_by(booking_status='confirmed').count()
        cancelled_bookings = session.query(Booking).filter_by(booking_status='cancelled').count()
        completed_bookings = session.query(Booking).filter_by(booking_status='completed').count()

# Occupancy
occupancy = AvailabilityChecker.get_occupancy_rate(start_date, today)


# ============================================================================
# KEY METRICS
# ============================================================================

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

st.markdown("""
<div class='solivie-card' style='margin-bottom: 1.5rem;'>
    <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
        📈 Key Performance Metrics
    </h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card' style='border-color: #C4935B;'>
        <div class='metric-label'>💰 Total Revenue</div>
        <div class='metric-value'>{format_currency(total_revenue)}</div>
        <div class='metric-subtitle'>{num_transactions} transactions</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card' style='border-color: #6B8E7E;'>
        <div class='metric-label'>📋 Bookings</div>
        <div class='metric-value'>{total_bookings}</div>
        <div class='metric-subtitle'>{confirmed_bookings} confirmed</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    occupancy_color = "#6B8E7E" if occupancy >= 70 else "#C4935B" if occupancy >= 50 else "#A95F5F"
    st.markdown(f"""
    <div class='metric-card' style='border-color: {occupancy_color};'>
        <div class='metric-label'>🏨 Occupancy</div>
        <div class='metric-value'>{occupancy:.1f}%</div>
        <div class='metric-subtitle'>Average rate</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card' style='border-color: #7B9CA8;'>
        <div class='metric-label'>👥 Total Users</div>
        <div class='metric-value'>{total_users}</div>
        <div class='metric-subtitle'>+{new_users} new</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# ROOM & BOOKING STATUS
# ============================================================================

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 1.5rem;'>
        <h3 style='color: #C4935B; margin: 0 0 1.5rem 0; font-size: 1.3rem;'>
            🛏️ Room Status Overview
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1a, col1b = st.columns(2)
    
    with col1a:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #6B8E7E;
                    margin-bottom: 1rem;'>
            <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem; font-weight: 600;'>🟢 Available</p>
            <p style='color: #6B8E7E; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{available_rooms}</p>
            <p style='color: #7B9CA8; margin: 0.25rem 0 0 0; font-size: 0.85rem;'>{get_percentage(available_rooms, total_rooms)}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #C4935B;
                    margin-bottom: 1rem;'>
            <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem; font-weight: 600;'>🔴 Occupied</p>
            <p style='color: #C4935B; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{occupied_rooms}</p>
            <p style='color: #7B9CA8; margin: 0.25rem 0 0 0; font-size: 0.85rem;'>{get_percentage(occupied_rooms, total_rooms)}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col1b:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #A95F5F;
                    margin-bottom: 1rem;'>
            <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem; font-weight: 600;'>🔧 Maintenance</p>
            <p style='color: #D4A76A; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{maintenance_rooms}</p>
            <p style='color: #7B9CA8; margin: 0.25rem 0 0 0; font-size: 0.85rem;'>{get_percentage(maintenance_rooms, total_rooms)}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #7B9CA8;
                    margin-bottom: 1rem;'>
            <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem; font-weight: 600;'>🧹 Cleaning</p>
            <p style='color: #7B9CA8; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{cleaning_rooms}</p>
            <p style='color: #7B9CA8; margin: 0.25rem 0 0 0; font-size: 0.85rem;'>{get_percentage(cleaning_rooms, total_rooms)}%</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 1.5rem;'>
        <h3 style='color: #C4935B; margin: 0 0 1.5rem 0; font-size: 1.3rem;'>
            📊 Booking Status Distribution
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col2a, col2b = st.columns(2)
    
    with col2a:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #C4935B;
                    margin-bottom: 1rem;'>
            <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem; font-weight: 600;'>⏳ Pending</p>
            <p style='color: #C4935B; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{pending_bookings}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #6B8E7E;
                    margin-bottom: 1rem;'>
            <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem; font-weight: 600;'>✅ Confirmed</p>
            <p style='color: #6B8E7E; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{confirmed_total}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2b:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #A95F5F;
                    margin-bottom: 1rem;'>
            <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem; font-weight: 600;'>❌ Cancelled</p>
            <p style='color: #D4A76A; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{cancelled_bookings}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #7B9CA8;
                    margin-bottom: 1rem;'>
            <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem; font-weight: 600;'>✓ Completed</p>
            <p style='color: #7B9CA8; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;'>{completed_bookings}</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# RECENT BOOKINGS
# ============================================================================

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

st.markdown("""
<div class='solivie-card' style='margin-bottom: 1.5rem;'>
    <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
        📋 Recent Bookings (Last 10)
    </h3>
</div>
""", unsafe_allow_html=True)

with get_db_session() as session:
    recent = session.query(Booking).order_by(Booking.created_at.desc()).limit(10).all()
    
    recent_data = []
    for booking in recent:
        room = session.query(Room).filter_by(room_id=booking.room_id).first()
        user = session.query(User).filter_by(user_id=booking.user_id).first()
        
        recent_data.append({
            'reference': booking.booking_reference,
            'room_number': room.room_number if room else 'N/A',
            'room_type': room.room_type if room else 'N/A',
            'user_name': f"{user.first_name} {user.last_name}" if user else 'N/A',
            'status': booking.booking_status,
            'created': booking.created_at.strftime("%b %d, %Y %I:%M %p")
        })

if recent_data:
    for data in recent_data:
        # Determine status badge
        if data['status'] == 'confirmed':
            status_class = 'status-confirmed'
            status_text = '✅ Confirmed'
        elif data['status'] == 'pending':
            status_class = 'status-pending'
            status_text = '⏳ Pending'
        elif data['status'] == 'cancelled':
            status_class = 'status-cancelled'
            status_text = '❌ Cancelled'
        else:
            status_class = 'status-completed'
            status_text = '✓ Completed'
        
        st.markdown(f"""
        <div class='booking-row'>
            <div style='flex: 1;'>
                <p style='color: #C4935B; margin: 0; font-weight: 700; font-size: 1rem;'>
                    {data['reference']}
                </p>
                <p style='color: #9BA8A5; margin: 0.25rem 0 0 0; font-size: 0.85rem;'>
                    {data['created']}
                </p>
            </div>
            <div style='flex: 1;'>
                <p style='color: #F5F5F0; margin: 0; font-weight: 600;'>
                    🏨 Room {data['room_number']}
                </p>
                <p style='color: #9BA8A5; margin: 0.25rem 0 0 0; font-size: 0.85rem;'>
                    {data['room_type']}
                </p>
            </div>
            <div style='flex: 1;'>
                <p style='color: #F5F5F0; margin: 0; font-weight: 600;'>
                    👤 {data['user_name']}
                </p>
            </div>
            <div>
                <span class='status-badge {status_class}'>
                    {status_text}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                padding: 2rem;
                border-radius: 12px;
                text-align: center;
                border: 2px solid #3D4A47;'>
        <p style='color: #9BA8A5; margin: 0; font-size: 1.1rem;'>
            📭 No recent bookings found
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# QUICK ACTIONS
# ============================================================================

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

st.markdown("""
<div class='solivie-card' style='margin-bottom: 1.5rem;'>
    <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
        ⚡ Quick Actions
    </h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🛏️ MANAGE ROOMS", use_container_width=True, type="primary", key="quick_rooms"):
        st.switch_page("pages/10_⚙️_Admin_Management.py")

with col2:
    if st.button("📋 BOOKINGS", use_container_width=True, type="primary", key="quick_bookings"):
        st.switch_page("pages/9_🏨_Admin_Operations.py")

with col3:
    if st.button("👥 MANAGE USERS", use_container_width=True, type="primary", key="quick_users"):
        st.switch_page("pages/10_⚙️_Admin_Management.py")

with col4:
    if st.button("📈 REPORTS", use_container_width=True, type="primary", key="quick_reports"):
        st.switch_page("pages/11_📈_Reports.py")


# ============================================================================
# FOOTER NAVIGATION
# ============================================================================

st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])

with col2:
    if st.button("🏠 HOME", use_container_width=True, type="secondary", key="footer_home"):
        st.switch_page("app.py")

with col3:
    if st.button("🚪 LOGOUT", use_container_width=True, type="secondary", key="footer_logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ============================================================================
# FOOTER
# ============================================================================

SolivieUI.footer()

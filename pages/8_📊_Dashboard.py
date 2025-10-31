"""
Admin dashboard page.
Displays key metrics, statistics, and system overview.
"""

import streamlit as st
from datetime import datetime, timedelta
from database.db_manager import get_db_session
from database.models import Booking, Room, User, Payment
from backend.booking.availability_checker import AvailabilityChecker
from utils.helpers import format_currency, get_percentage
import config

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

if not st.session_state.get('is_admin', False):
    st.error("❌ Admin access required")
    if st.button("🏠 Go Home"):
        st.switch_page("app.py")
    st.stop()

st.title("📊 Admin Dashboard")
st.write(f"Welcome, {st.session_state.user_name} ({st.session_state.admin_role.upper()})")

# Date range selector
col1, col2 = st.columns([3, 1])
with col1:
    date_range = st.selectbox("Period", ["Today", "Last 7 Days", "Last 30 Days", "This Month"])
with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

# Calculate date range
today = datetime.now()
if date_range == "Today":
    start_date = today.replace(hour=0, minute=0, second=0)
elif date_range == "Last 7 Days":
    start_date = today - timedelta(days=7)
elif date_range == "Last 30 Days":
    start_date = today - timedelta(days=30)
else:
    start_date = today.replace(day=1, hour=0, minute=0, second=0)

st.markdown("---")

# Key metrics
with get_db_session() as session:
    payments = session.query(Payment).filter(
        Payment.payment_status == 'completed',
        Payment.payment_date >= start_date
    ).all()
    total_revenue = sum(p.amount for p in payments)
    
    bookings = session.query(Booking).filter(Booking.created_at >= start_date).all()
    total_bookings = len(bookings)
    confirmed = len([b for b in bookings if b.booking_status == 'confirmed'])
    
    total_rooms = session.query(Room).count()
    available_rooms = session.query(Room).filter_by(status='available').count()
    
    total_users = session.query(User).count()
    new_users = session.query(User).filter(User.created_at >= start_date).count()

occupancy = AvailabilityChecker.get_occupancy_rate(start_date, today)

st.markdown("### 📈 Key Metrics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Revenue", format_currency(total_revenue), f"{len(payments)} transactions")
col2.metric("📋 Bookings", total_bookings, f"{confirmed} confirmed")
col3.metric("🏨 Occupancy", f"{occupancy:.1f}%", "Average")
col4.metric("👥 Users", total_users, f"+{new_users} new")

st.markdown("---")

# Room statistics
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🛏️ Room Status")
    with get_db_session() as session:
        occupied = session.query(Room).filter_by(status='occupied').count()
        maintenance = session.query(Room).filter_by(status='maintenance').count()
        cleaning = session.query(Room).filter_by(status='cleaning').count()
    
    col1a, col1b, col1c = st.columns(3)
    col1a.metric("Available", available_rooms, f"{get_percentage(available_rooms, total_rooms)}%")
    col1b.metric("Occupied", occupied, f"{get_percentage(occupied, total_rooms)}%")
    col1c.metric("Maintenance", maintenance + cleaning)

with col2:
    st.markdown("### 📊 Booking Status")
    with get_db_session() as session:
        pending = session.query(Booking).filter_by(booking_status='pending').count()
        confirmed = session.query(Booking).filter_by(booking_status='confirmed').count()
        cancelled = session.query(Booking).filter_by(booking_status='cancelled').count()
        completed = session.query(Booking).filter_by(booking_status='completed').count()
    
    col2a, col2b = st.columns(2)
    col2a.metric("⏳ Pending", pending)
    col2a.metric("✅ Confirmed", confirmed)
    col2b.metric("❌ Cancelled", cancelled)
    col2b.metric("✓ Completed", completed)

st.markdown("---")

# Recent bookings
st.markdown("### 📋 Recent Bookings")

with get_db_session() as session:
    recent = session.query(Booking).order_by(Booking.created_at.desc()).limit(10).all()
    
    # ✅ FIX: Extract all data within the session
    recent_data = []
    for booking in recent:
        room = session.query(Room).filter_by(room_id=booking.room_id).first()
        user = session.query(User).filter_by(user_id=booking.user_id).first()
        
        recent_data.append({
            'reference': booking.booking_reference,
            'room_number': room.room_number if room else 'N/A',
            'user_name': f"{user.first_name} {user.last_name}" if user else 'N/A',
            'status': booking.booking_status
        })

if recent_data:
    for data in recent_data:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        col1.write(f"**{data['reference']}**")
        col2.write(f"Room {data['room_number']}")
        col3.write(data['user_name'])
        col4.write("🟢" if data['status'] == 'confirmed' else "🟡")
else:
    st.info("No recent bookings")

st.markdown("---")

# Quick actions
st.markdown("### ⚡ Quick Actions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🛏️ Manage Rooms", use_container_width=True):
        st.switch_page("pages/9_🛏️_Manage_Rooms.py")
with col2:
    if st.button("📋 Bookings", use_container_width=True):
        st.switch_page("pages/10_📋_Manage_Bookings.py")
with col3:
    if st.button("👥 Users", use_container_width=True):
        st.switch_page("pages/11_👥_Manage_Users.py")
with col4:
    if st.button("📈 Reports", use_container_width=True):
        st.switch_page("pages/12_📈_Reports.py")

st.markdown("---")

if st.button("🚪 Logout", use_container_width=True, type="secondary"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

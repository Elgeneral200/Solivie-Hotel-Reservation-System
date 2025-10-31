"""
Reports and analytics page.
Generate various reports and statistics.
"""

import streamlit as st
from datetime import datetime, timedelta
from database.db_manager import get_db_session
from database.models import Booking, Payment, Room
from utils.helpers import format_currency
from backend.booking.availability_checker import AvailabilityChecker

st.set_page_config(page_title="Reports", page_icon="📈", layout="wide")

if not st.session_state.get('is_admin', False):
    st.error("❌ Admin access required")
    st.stop()

st.title("📈 Reports & Analytics")

# Date range
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
with col2:
    end_date = st.date_input("End Date", value=datetime.now())

start_dt = datetime.combine(start_date, datetime.min.time())
end_dt = datetime.combine(end_date, datetime.max.time())

if st.button("📊 Generate Report", use_container_width=True, type="primary"):
    with st.spinner("Generating..."):
        
        # Revenue report
        st.markdown("### 💰 Revenue Report")
        with get_db_session() as session:
            payments = session.query(Payment).filter(
                Payment.payment_status == 'completed',
                Payment.payment_date >= start_dt,
                Payment.payment_date <= end_dt
            ).all()
            
            total_revenue = sum(p.amount for p in payments)
            avg_transaction = total_revenue / len(payments) if payments else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Revenue", format_currency(total_revenue))
            col2.metric("Transactions", len(payments))
            col3.metric("Average", format_currency(avg_transaction))
        
        st.markdown("---")
        
        # Booking report
        st.markdown("### 📋 Booking Report")
        with get_db_session() as session:
            bookings = session.query(Booking).filter(
                Booking.created_at >= start_dt,
                Booking.created_at <= end_dt
            ).all()
            
            by_status = {}
            for booking in bookings:
                by_status[booking.booking_status] = by_status.get(booking.booking_status, 0) + 1
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total", len(bookings))
            col2.metric("Confirmed", by_status.get('confirmed', 0))
            col3.metric("Cancelled", by_status.get('cancelled', 0))
            col4.metric("Completed", by_status.get('completed', 0))
        
        st.markdown("---")
        
        # Occupancy report
        st.markdown("### 🏨 Occupancy Report")
        occupancy = AvailabilityChecker.get_occupancy_rate(start_dt, end_dt)
        
        col1, col2 = st.columns(2)
        col1.metric("Occupancy Rate", f"{occupancy:.1f}%")
        
        with get_db_session() as session:
            total_rooms = session.query(Room).count()
            nights = (end_dt - start_dt).days
            total_room_nights = total_rooms * nights
            
            col2.metric("Total Room-Nights", total_room_nights)

"""
Reports and Analytics - Dark Luxury Theme
Generate comprehensive reports and statistics
Enhanced with professional styling and data visualization
"""
import streamlit as st
from datetime import datetime, timedelta
from database.db_manager import get_db_session
from database.models import Booking, Payment, Room, User
from utils.ui_components import SolivieUI
from utils.helpers import format_currency
from backend.booking.availability_checker import AvailabilityChecker


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Reports & Analytics - Solivie Hotel",
    page_icon="📈",
    layout="wide"
)

# Apply dark luxury CSS
SolivieUI.inject_custom_css()

# Additional reports-specific styling
st.markdown("""
<style>
/* ===== REPORT SECTIONS ===== */
.report-section {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 2rem;
    border-radius: 15px;
    border: 2px solid #C4935B;
    margin-bottom: 2rem;
}

.report-metric {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 1.5rem;
    border-radius: 12px;
    border: 2px solid #3D4A47;
    text-align: center;
    transition: all 0.3s ease;
}

.report-metric:hover {
    border-color: #C4935B;
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(196, 147, 91, 0.3);
}

.metric-value-large {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #C4935B 0%, #D4A76A 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.5rem 0;
}

.metric-label-large {
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

/* ===== COMPARISON BARS ===== */
.comparison-bar {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 1rem;
    border-radius: 10px;
    border: 2px solid #3D4A47;
    margin-bottom: 1rem;
}

.progress-bar {
    background: linear-gradient(145deg, #3D4A47 0%, #2A3533 100%);
    height: 30px;
    border-radius: 8px;
    overflow: hidden;
    position: relative;
}

.progress-fill {
    background: linear-gradient(90deg, #C4935B 0%, #D4A76A 100%);
    height: 100%;
    border-radius: 8px;
    transition: width 0.5s ease;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 10px;
}

/* ===== SUMMARY CARDS ===== */
.summary-card {
    background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
    padding: 1.5rem;
    border-radius: 12px;
    border: 2px solid #C4935B;
    text-align: center;
}

.summary-value {
    font-size: 2rem;
    font-weight: 700;
    color: #C4935B;
    margin: 0.5rem 0;
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
            You need administrator privileges to access reports
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 LOGIN AS ADMIN", use_container_width=True, type="primary", key="reports_login"):
            st.switch_page("pages/2_🔐_Login.py")
    with col2:
        if st.button("🏠 HOME", use_container_width=True, type="secondary", key="reports_home"):
            st.switch_page("app.py")
    st.stop()


# ============================================================================
# PAGE HEADER
# ============================================================================

SolivieUI.page_header(
    "Reports & Analytics",
    "Comprehensive business intelligence and performance metrics",
    "📈"
)


# ============================================================================
# DATE RANGE SELECTOR
# ============================================================================

st.markdown("""
<div class='solivie-card' style='margin-bottom: 2rem;'>
    <h3 style='color: #C4935B; margin: 0 0 1.5rem 0; font-size: 1.5rem;'>
        📅 Select Reporting Period
    </h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    start_date = st.date_input(
        "📅 Start Date",
        value=datetime.now() - timedelta(days=30),
        key="report_start_date"
    )

with col2:
    end_date = st.date_input(
        "📅 End Date",
        value=datetime.now(),
        key="report_end_date"
    )

with col3:
    st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
    quick_range = st.selectbox(
        "⚡ Quick Select",
        ["Custom", "Last 7 Days", "Last 30 Days", "This Month", "Last Month"],
        key="quick_range"
    )

# Apply quick range
if quick_range != "Custom":
    today = datetime.now().date()
    if quick_range == "Last 7 Days":
        start_date = today - timedelta(days=7)
        end_date = today
    elif quick_range == "Last 30 Days":
        start_date = today - timedelta(days=30)
        end_date = today
    elif quick_range == "This Month":
        start_date = today.replace(day=1)
        end_date = today
    elif quick_range == "Last Month":
        last_month = today.replace(day=1) - timedelta(days=1)
        start_date = last_month.replace(day=1)
        end_date = last_month

start_dt = datetime.combine(start_date, datetime.min.time())
end_dt = datetime.combine(end_date, datetime.max.time())

# Calculate days
days_span = (end_date - start_date).days + 1

st.markdown(f"""
<div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            border: 2px solid #C4935B;
            margin-bottom: 2rem;'>
    <p style='color: #C4935B; margin: 0; font-weight: 600;'>
        📊 Reporting Period: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')} ({days_span} days)
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# GENERATE REPORT BUTTON
# ============================================================================

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    generate_btn = st.button(
        "📊 GENERATE COMPREHENSIVE REPORT",
        use_container_width=True,
        type="primary",
        key="generate_report_btn"
    )

if generate_btn or 'report_generated' not in st.session_state:
    st.session_state.report_generated = True

if st.session_state.get('report_generated', False):
    with st.spinner("📊 Generating comprehensive report..."):
        
        # ====================================================================
        # REVENUE REPORT
        # ====================================================================
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='report-section'>
            <h3 style='color: #C4935B; margin: 0 0 2rem 0; font-size: 2rem;'>
                💰 Revenue Analysis
            </h3>
        """, unsafe_allow_html=True)
        
        with get_db_session() as session:
            payments = session.query(Payment).filter(
                Payment.payment_status == 'completed',
                Payment.payment_date >= start_dt,
                Payment.payment_date <= end_dt
            ).all()
            
            total_revenue = sum(p.amount for p in payments)
            num_transactions = len(payments)
            avg_transaction = total_revenue / num_transactions if num_transactions else 0
            
            # Revenue by payment method
            revenue_by_method = {}
            for p in payments:
                method = p.payment_method or 'Unknown'
                revenue_by_method[method] = revenue_by_method.get(method, 0) + p.amount
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #C4935B;'>
                <div class='metric-label-large'>💰 Total Revenue</div>
                <div class='metric-value-large'>{format_currency(total_revenue)}</div>
                <div class='metric-subtitle'>{days_span} days</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #6B8E7E;'>
                <div class='metric-label-large'>💳 Transactions</div>
                <div class='metric-value-large'>{num_transactions}</div>
                <div class='metric-subtitle'>Completed payments</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #7B9CA8;'>
                <div class='metric-label-large'>📊 Average</div>
                <div class='metric-value-large'>{format_currency(avg_transaction)}</div>
                <div class='metric-subtitle'>Per transaction</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            daily_avg = total_revenue / days_span if days_span > 0 else 0
            st.markdown(f"""
            <div class='report-metric' style='border-color: #C4935B;'>
                <div class='metric-label-large'>📅 Daily Average</div>
                <div class='metric-value-large'>{format_currency(daily_avg)}</div>
                <div class='metric-subtitle'>Per day</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Revenue by payment method
        if revenue_by_method:
            st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: #C4935B;'>💳 Revenue by Payment Method</h4>", unsafe_allow_html=True)
            
            for method, amount in sorted(revenue_by_method.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total_revenue * 100) if total_revenue > 0 else 0
                st.markdown(f"""
                <div class='comparison-bar'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                        <span style='color: #F5F5F0; font-weight: 600;'>{method}</span>
                        <span style='color: #C4935B; font-weight: 700;'>{format_currency(amount)} ({percentage:.1f}%)</span>
                    </div>
                    <div class='progress-bar'>
                        <div class='progress-fill' style='width: {percentage}%;'>
                            <span style='color: #1A1F1E; font-weight: 700; font-size: 0.85rem;'>{percentage:.1f}%</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ====================================================================
        # BOOKING REPORT
        # ====================================================================
        
        st.markdown("""
        <div class='report-section'>
            <h3 style='color: #C4935B; margin: 0 0 2rem 0; font-size: 2rem;'>
                📋 Booking Performance
            </h3>
        """, unsafe_allow_html=True)
        
        with get_db_session() as session:
            bookings = session.query(Booking).filter(
                Booking.created_at >= start_dt,
                Booking.created_at <= end_dt
            ).all()
            
            total_bookings = len(bookings)
            
            by_status = {}
            revenue_by_status = {}
            for booking in bookings:
                status = booking.booking_status
                by_status[status] = by_status.get(status, 0) + 1
                revenue_by_status[status] = revenue_by_status.get(status, 0) + booking.total_amount
            
            confirmed = by_status.get('confirmed', 0)
            pending = by_status.get('pending', 0)
            cancelled = by_status.get('cancelled', 0)
            completed = by_status.get('completed', 0)
            
            # Calculate cancellation rate
            cancellation_rate = (cancelled / total_bookings * 100) if total_bookings > 0 else 0
            completion_rate = (completed / total_bookings * 100) if total_bookings > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #C4935B;'>
                <div class='metric-label-large'>📊 Total Bookings</div>
                <div class='metric-value-large'>{total_bookings}</div>
                <div class='metric-subtitle'>{days_span} days</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #6B8E7E;'>
                <div class='metric-label-large'>✅ Confirmed</div>
                <div class='metric-value-large'>{confirmed}</div>
                <div class='metric-subtitle'>{(confirmed/total_bookings*100) if total_bookings else 0:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #A95F5F;'>
                <div class='metric-label-large'>❌ Cancelled</div>
                <div class='metric-value-large'>{cancelled}</div>
                <div class='metric-subtitle'>{cancellation_rate:.1f}% rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #7B9CA8;'>
                <div class='metric-label-large'>✓ Completed</div>
                <div class='metric-value-large'>{completed}</div>
                <div class='metric-subtitle'>{completion_rate:.1f}% rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Booking status breakdown
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #C4935B;'>📊 Booking Status Breakdown</h4>", unsafe_allow_html=True)
        
        status_colors = {
            'confirmed': '#6B8E7E',
            'pending': '#C4935B',
            'cancelled': '#A95F5F',
            'completed': '#7B9CA8'
        }
        
        for status, count in sorted(by_status.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_bookings * 100) if total_bookings > 0 else 0
            revenue = revenue_by_status.get(status, 0)
            color = status_colors.get(status, '#9BA8A5')
            
            st.markdown(f"""
            <div class='comparison-bar'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                    <span style='color: #F5F5F0; font-weight: 600; text-transform: uppercase;'>{status}</span>
                    <span style='color: {color}; font-weight: 700;'>{count} bookings • {format_currency(revenue)}</span>
                </div>
                <div class='progress-bar'>
                    <div class='progress-fill' style='width: {percentage}%; background: linear-gradient(90deg, {color} 0%, {color}AA 100%);'>
                        <span style='color: #1A1F1E; font-weight: 700; font-size: 0.85rem;'>{percentage:.1f}%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ====================================================================
        # OCCUPANCY REPORT
        # ====================================================================
        
        st.markdown("""
        <div class='report-section'>
            <h3 style='color: #C4935B; margin: 0 0 2rem 0; font-size: 2rem;'>
                🏨 Occupancy & Capacity Analysis
            </h3>
        """, unsafe_allow_html=True)
        
        occupancy = AvailabilityChecker.get_occupancy_rate(start_dt, end_dt)
        
        with get_db_session() as session:
            total_rooms = session.query(Room).count()
            available_rooms = session.query(Room).filter_by(status='available').count()
            occupied_rooms = session.query(Room).filter_by(status='occupied').count()
            
            nights = (end_dt - start_dt).days
            total_room_nights = total_rooms * nights
            occupied_room_nights = int((occupancy / 100) * total_room_nights)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            occupancy_color = "#6B8E7E" if occupancy >= 70 else "#C4935B" if occupancy >= 50 else "#A95F5F"
            st.markdown(f"""
            <div class='report-metric' style='border-color: {occupancy_color};'>
                <div class='metric-label-large'>📊 Occupancy Rate</div>
                <div class='metric-value-large'>{occupancy:.1f}%</div>
                <div class='metric-subtitle'>Average rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #C4935B;'>
                <div class='metric-label-large'>🏨 Total Rooms</div>
                <div class='metric-value-large'>{total_rooms}</div>
                <div class='metric-subtitle'>In property</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #6B8E7E;'>
                <div class='metric-label-large'>🌙 Room-Nights</div>
                <div class='metric-value-large'>{total_room_nights}</div>
                <div class='metric-subtitle'>{nights} nights × {total_rooms} rooms</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #7B9CA8;'>
                <div class='metric-label-large'>✅ Occupied</div>
                <div class='metric-value-large'>{occupied_room_nights}</div>
                <div class='metric-subtitle'>Room-nights sold</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Current room status
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #C4935B;'>🏨 Current Room Status</h4>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            available_pct = (available_rooms / total_rooms * 100) if total_rooms > 0 else 0
            st.markdown(f"""
            <div class='summary-card' style='border-color: #6B8E7E;'>
                <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem; font-weight: 600;'>✅ AVAILABLE</p>
                <p class='summary-value' style='color: #6B8E7E;'>{available_rooms}</p>
                <p style='color: #7B9CA8; margin: 0; font-size: 0.85rem;'>{available_pct:.1f}% of total</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            occupied_pct = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
            st.markdown(f"""
            <div class='summary-card' style='border-color: #A95F5F;'>
                <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem; font-weight: 600;'>🔴 OCCUPIED</p>
                <p class='summary-value' style='color: #D4A76A;'>{occupied_rooms}</p>
                <p style='color: #7B9CA8; margin: 0; font-size: 0.85rem;'>{occupied_pct:.1f}% of total</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            other_rooms = total_rooms - available_rooms - occupied_rooms
            other_pct = (other_rooms / total_rooms * 100) if total_rooms > 0 else 0
            st.markdown(f"""
            <div class='summary-card' style='border-color: #C4935B;'>
                <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem; font-weight: 600;'>🔧 MAINTENANCE</p>
                <p class='summary-value'>{other_rooms}</p>
                <p style='color: #7B9CA8; margin: 0; font-size: 0.85rem;'>{other_pct:.1f}% of total</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ====================================================================
        # USER STATISTICS
        # ====================================================================
        
        st.markdown("""
        <div class='report-section'>
            <h3 style='color: #C4935B; margin: 0 0 2rem 0; font-size: 2rem;'>
                👥 User Statistics
            </h3>
        """, unsafe_allow_html=True)
        
        with get_db_session() as session:
            total_users = session.query(User).count()
            active_users = session.query(User).filter_by(account_status='active').count()
            new_users = session.query(User).filter(
                User.created_at >= start_dt,
                User.created_at <= end_dt
            ).count()
            users_with_bookings = session.query(User).join(Booking).filter(
                Booking.created_at >= start_dt,
                Booking.created_at <= end_dt
            ).distinct().count()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #7B9CA8;'>
                <div class='metric-label-large'>👥 Total Users</div>
                <div class='metric-value-large'>{total_users}</div>
                <div class='metric-subtitle'>Registered</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #6B8E7E;'>
                <div class='metric-label-large'>✅ Active Users</div>
                <div class='metric-value-large'>{active_users}</div>
                <div class='metric-subtitle'>{(active_users/total_users*100) if total_users else 0:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='report-metric' style='border-color: #C4935B;'>
                <div class='metric-label-large'>⭐ New Users</div>
                <div class='metric-value-large'>{new_users}</div>
                <div class='metric-subtitle'>In period</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            booking_rate = (users_with_bookings / new_users * 100) if new_users > 0 else 0
            st.markdown(f"""
            <div class='report-metric' style='border-color: #7B9CA8;'>
                <div class='metric-label-large'>📋 Active Bookers</div>
                <div class='metric-value-large'>{users_with_bookings}</div>
                <div class='metric-subtitle'>{booking_rate:.1f}% conversion</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ====================================================================
        # SUMMARY
        # ====================================================================
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Safely format dates
        try:
            start_date_formatted = start_date.strftime('%B %d, %Y')
            end_date_formatted = end_date.strftime('%B %d, %Y')
        except AttributeError:
            # Fallback if date objects don't have strftime
            start_date_formatted = str(start_date)
            end_date_formatted = str(end_date)
        
        current_datetime = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                    padding: 2rem;
                    border-radius: 15px;
                    border: 3px solid #C4935B;
                    text-align: center;
                    margin-top: 2rem;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.5);'>
            <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 1.8rem;'>
                📊 Report Summary
            </h3>
            <p style='color: #F5F5F0; margin: 0.5rem 0; font-size: 1.1rem;'>
                Report generated successfully for the period of <strong>{start_date_formatted}</strong> to <strong>{end_date_formatted}</strong>
            </p>
            <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
                📅 Generated on {current_datetime}
            </p>
            <p style='color: #7B9CA8; margin: 0.5rem 0 0 0; font-size: 0.85rem;'>
                ⏱️ Report span: {days_span} days
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
    if st.button("🏨 OPERATIONS", use_container_width=True, type="secondary", key="footer_ops"):
        st.switch_page("pages/9_🏨_Admin_Operations.py")

with col4:
    if st.button("🚪 LOGOUT", use_container_width=True, type="secondary", key="footer_logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ============================================================================
# FOOTER
# ============================================================================

SolivieUI.footer()

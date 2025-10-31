"""
Booking completion page - FINAL FIXED VERSION
"""
import streamlit as st
from backend.booking.booking_manager import BookingManager
from backend.payment.payment_processor import PaymentProcessor
from backend.user.user_manager import UserManager
from utils.helpers import format_currency, format_datetime
import config

st.set_page_config(page_title="Book Room", page_icon="📅", layout="wide")

if not st.session_state.get('logged_in'):
    st.error("❌ Please login to make a booking")
    if st.button("🔐 Login"):
        st.switch_page("pages/2_🔐_Login.py")
    st.stop()

if 'booking_data' not in st.session_state:
    st.warning("⚠️ No room selected")
    if st.button("🔍 Search Rooms"):
        st.switch_page("pages/4_🔍_Search_Rooms.py")
    st.stop()

booking_data = st.session_state.booking_data
user = UserManager.get_user_profile(st.session_state.user_id)

if not user:
    st.error("User not found")
    st.stop()

st.title("📅 Complete Your Booking")

col1, col2 = st.columns([2, 1])

with col1:
    with st.form("booking_form", clear_on_submit=False):
        st.markdown("### 👤 Guest Details")
        st.text_input("Full Name", value=f"{user['first_name']} {user['last_name']}", disabled=True)
        st.text_input("Email", value=user['email'], disabled=True)
        
        st.markdown("### 💬 Special Requests")
        special_requests = st.text_area("Any special requirements?", height=100, key="special_req")
        
        st.markdown("### 🎁 Promo Code")
        promo_code = st.text_input("Promo code (optional)", key="promo_code_input")
        if promo_code:
            st.caption("Available: WELCOME10 (10% off), SUMMER2025 (15% off)")
        
        st.markdown("### 💳 Payment Method")
        payment_method = st.selectbox("Payment Method", config.PAYMENT_METHODS, key="payment_method")
        
        card_number = ""
        card_expiry = ""
        card_cvv = ""
        
        if payment_method in ["Credit Card", "Debit Card"]:
            st.markdown("#### Card Details")
            card_number = st.text_input("Card Number", type="password", key="card_number_input", placeholder="4532015112830366")
            col1a, col1b = st.columns(2)
            with col1a:
                card_expiry = st.text_input("Expiry (MM/YY)", key="card_expiry_input", placeholder="12/28")
            with col1b:
                card_cvv = st.text_input("CVV", type="password", key="card_cvv_input", placeholder="123")
            st.caption("🔒 Test: 4532015112830366 | 12/28 | 123")
        
        agree = st.checkbox("✅ I agree to Terms & Conditions", key="agree_checkbox")
        
        # ✅ FIX: Only form_submit_button inside form
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit = st.form_submit_button("🎉 Confirm Booking", use_container_width=True, type="primary")
        with col_btn2:
            cancel = st.form_submit_button("❌ Cancel Booking", use_container_width=True)
        
        if cancel:
            if 'booking_data' in st.session_state:
                del st.session_state.booking_data
            st.switch_page("pages/4_🔍_Search_Rooms.py")
        
        if submit:
            if not agree:
                st.error("❌ Must agree to Terms & Conditions")
            elif payment_method in ["Credit Card", "Debit Card"] and not card_number:
                st.error("❌ Please enter card details")
            else:
                with st.spinner("⏳ Processing your booking..."):
                    # Create booking
                    success, booking_id, msg = BookingManager.create_booking(
                        st.session_state.user_id,
                        booking_data['room_id'],
                        booking_data['check_in'],
                        booking_data['check_out'],
                        booking_data['num_guests'],
                        special_requests,
                        promo_code
                    )
                    
                    if success:
                        # Get booking as dictionary
                        booking = BookingManager.get_booking(booking_id=booking_id)
                        
                        if booking:
                            # Process payment
                            pay_success, pay_msg = PaymentProcessor.process_payment(
                                booking_id,
                                booking['total_amount'],
                                payment_method
                            )
                            
                            if pay_success:
                                st.success("✅ Booking Confirmed!")
                                st.info(f"📋 Booking Reference: **{booking['booking_reference']}**")
                                st.info(f"💰 Total Paid: {format_currency(booking['total_amount'])}")
                                st.balloons()
                                if 'booking_data' in st.session_state:
                                    del st.session_state.booking_data
                                
                                # ✅ FIX: Buttons OUTSIDE form
                                st.markdown("---")
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("📋 My Bookings", use_container_width=True, type="primary"):
                                        st.switch_page("pages/6_👤_My_Profile.py")
                                with col_b:
                                    if st.button("🏠 Home", use_container_width=True):
                                        st.switch_page("app.py")
                            else:
                                st.error(f"❌ Payment failed: {pay_msg}")
                        else:
                            st.error("❌ Could not retrieve booking details")
                    else:
                        st.error(f"❌ {msg}")

with col2:
    st.markdown("### 📋 Summary")
    st.markdown(f"""
    **🏨 Room {booking_data['room_number']}**
    {booking_data['room_type']}
    
    **👥 Guests:** {booking_data['num_guests']}
    
    **📅 Nights:** {booking_data['nights']}
    
    **💰 Total:** {format_currency(booking_data['total_price'])}
    """)

# ✅ FIX: Add logout button OUTSIDE form at bottom
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col3:
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

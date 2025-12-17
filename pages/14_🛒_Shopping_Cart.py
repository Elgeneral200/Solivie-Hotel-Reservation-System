"""
Shopping Cart - Multiple Room Booking
"""
import streamlit as st
from backend.booking.cart_manager import CartManager
from backend.booking.booking_manager import BookingManager
from backend.payment.payment_processor import PaymentProcessor
from utils.helpers import format_currency, format_datetime
from datetime import datetime


st.set_page_config(page_title="Shopping Cart", page_icon="🛒", layout="wide")


if not st.session_state.get('logged_in'):
    st.error("❌ Please login to view cart")
    st.stop()


# Initialize cart
CartManager.init_cart(st.session_state)


st.title("🛒 Shopping Cart")


# Get cart info
cart_count = CartManager.get_cart_count(st.session_state)
cart_total = CartManager.get_cart_total(st.session_state)
total_guests = CartManager.get_total_guests(st.session_state)


# ===== EMPTY CART =====
if cart_count == 0:
    st.info("🛒 Your cart is empty")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Search Rooms", use_container_width=True, type="primary"):
            st.switch_page("pages/2_🔍_Search_Rooms.py")
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    st.stop()


# ===== CART SUMMARY =====
st.markdown("### 📋 Cart Summary")
col1, col2, col3, col4 = st.columns(4)

col1.metric("🛏️ Total Rooms", cart_count)
col2.metric("👥 Total Guests", total_guests)
col3.metric("📅 Check-in", st.session_state.cart_check_in.strftime('%b %d, %Y') if st.session_state.cart_check_in else "N/A")
col4.metric("📅 Check-out", st.session_state.cart_check_out.strftime('%b %d, %Y') if st.session_state.cart_check_out else "N/A")

st.markdown("---")


# ===== CART ITEMS =====
st.markdown("### 🛏️ Rooms in Cart")

for idx, item in enumerate(st.session_state.cart):
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"#### 🏨 Room {item['room_number']} - {item['room_type']}")
            st.write(f"**Capacity:** {item['capacity']} guests | **Guests:** {item['num_guests']}")
            st.caption(item['description'])
        
        with col2:
            st.metric("Per Night", format_currency(item['base_price']))
            st.metric(f"Total ({item['nights']} nights)", format_currency(item['total_price']))
        
        with col3:
            st.markdown("")
            st.markdown("")
            if st.button("🗑️ Remove", key=f"remove_{item['room_id']}", use_container_width=True, type="secondary"):
                CartManager.remove_from_cart(st.session_state, item['room_id'])
                st.success("Room removed from cart")
                st.rerun()
        
        st.markdown("---")


# ===== CART TOTAL =====
st.markdown("### 💰 Total Amount")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"""
    - **Number of Rooms:** {cart_count}
    - **Total Guests:** {total_guests}
    - **Check-in:** {format_datetime(st.session_state.cart_check_in)}
    - **Check-out:** {format_datetime(st.session_state.cart_check_out)}
    - **Total Nights:** {st.session_state.cart[0]['nights']} per room
    """)

with col2:
    st.markdown("")
    st.markdown("")
    st.markdown(f"## **{format_currency(cart_total)}**")
    st.caption("Total for all rooms")


st.markdown("---")


# ===== ACTIONS =====
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔍 Continue Shopping", use_container_width=True, type="secondary"):
        st.switch_page("pages/2_🔍_Search_Rooms.py")

with col2:
    if st.button("🗑️ Clear Cart", use_container_width=True, type="secondary"):
        CartManager.clear_cart(st.session_state)
        st.success("Cart cleared!")
        st.rerun()

with col3:
    if st.button("💳 Proceed to Checkout", use_container_width=True, type="primary"):
        st.session_state.show_checkout = True
        st.rerun()


# ===== CHECKOUT PROCESS =====
if st.session_state.get('show_checkout', False):
    st.markdown("---")
    st.markdown("### 💳 Checkout - Multiple Room Booking")
    st.markdown(f"**Total Amount:** {format_currency(cart_total)}")
    
    payment_method = st.selectbox(
        "Payment Method",
        ["Credit Card", "Debit Card", "PayPal", "Bank Transfer"],
        key="payment_method_input"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456", key="card_number_input")
    with col2:
        card_cvv = st.text_input("CVV", type="password", placeholder="123", key="card_cvv_input")
    
    col1, col2 = st.columns(2)
    with col1:
        card_expiry = st.text_input("Expiry (MM/YY)", placeholder="12/25", key="card_expiry_input")
    with col2:
        card_name = st.text_input("Cardholder Name", placeholder="John Doe", key="card_name_input")
    
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("❌ Cancel", use_container_width=True, type="secondary", key="cancel_checkout"):
            st.session_state.show_checkout = False
            st.rerun()
    
    with col2:
        if st.button("💳 Pay & Book All Rooms", use_container_width=True, type="primary", key="submit_payment_btn"):
            if not all([card_number, card_cvv, card_expiry, card_name]):
                st.error("❌ Please fill in all payment details")
            else:
                with st.spinner("Processing multiple bookings..."):
                    booking_refs = []
                    all_success = True
                    
                    for idx, item in enumerate(st.session_state.cart):
                        try:
                            # Create booking
                            success, booking_id, message = BookingManager.create_booking(
                                st.session_state.user_id,
                                item['room_id'],
                                st.session_state.cart_check_in,
                                st.session_state.cart_check_out,
                                item['num_guests'],
                                f"Group booking - {cart_count} rooms",
                                ""
                            )
                            
                            if not success:
                                st.error(f"❌ Failed to book Room {item['room_number']}: {message}")
                                all_success = False
                                break
                            
                            # Process payment
                            payment_success, payment_msg = PaymentProcessor.process_payment(
                                booking_id,
                                item['total_price'],
                                payment_method
                            )
                            
                            if not payment_success:
                                st.error(f"❌ Payment failed for Room {item['room_number']}: {payment_msg}")
                                all_success = False
                                break
                            
                            # Get booking reference
                            from database.db_manager import get_db_session
                            from database.models import Booking
                            
                            with get_db_session() as session:
                                booking_obj = session.query(Booking).filter_by(booking_id=booking_id).first()
                                if booking_obj:
                                    booking_refs.append(booking_obj.booking_reference)
                        
                        except Exception as e:
                            st.error(f"❌ ERROR processing Room {item['room_number']}: {str(e)}")
                            all_success = False
                            break
                    
                    if all_success:
                        st.success(f"🎉 Successfully booked {len(booking_refs)} rooms!")
                        st.balloons()
                        
                        st.markdown("### 📋 Booking References:")
                        for ref in booking_refs:
                            st.code(ref, language=None)
                        
                        st.info("📧 Confirmation emails have been sent for all bookings!")
                        
                        # Clear cart
                        CartManager.clear_cart(st.session_state)
                        st.session_state.show_checkout = False
                        
                        st.markdown("---")
                        if st.button("📋 View My Bookings", use_container_width=True, type="primary"):
                            st.switch_page("pages/6_👤_My_Profile.py")
                    else:
                        st.error("⚠️ Some bookings failed. Please contact support.")


# Logout
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col3:
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

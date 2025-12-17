"""
Shopping Cart - Complete Booking System (Single + Multiple Rooms)
Dark Luxury Theme - Handles all booking functionality
"""
import streamlit as st
from backend.booking.cart_manager import CartManager
from backend.booking.booking_manager import BookingManager
from backend.payment.payment_processor import PaymentProcessor
from backend.user.user_manager import UserManager
from utils.ui_components import SolivieUI
from utils.helpers import format_currency, format_datetime
from datetime import datetime
import config


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Shopping Cart - Solivie Hotel",
    page_icon="🛒",
    layout="wide"
)

# Apply dark luxury CSS
SolivieUI.inject_custom_css()


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
            Please login to access your shopping cart
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔐 LOGIN NOW", use_container_width=True, type="primary", key="cart_login"):
            st.switch_page("pages/2_🔐_Login.py")
    st.stop()


# ============================================================================
# INITIALIZE CART & USER DATA
# ============================================================================

CartManager.init_cart(st.session_state)
user = UserManager.get_user_profile(st.session_state.user_id)

if not user:
    st.error("❌ User profile not found")
    st.stop()


# ============================================================================
# CART SUMMARY & VALIDATION
# ============================================================================

cart_count = CartManager.get_cart_count(st.session_state)
cart_total = CartManager.get_cart_total(st.session_state)
total_guests = CartManager.get_total_guests(st.session_state)


# ===== EMPTY CART HANDLING =====
if cart_count == 0:
    SolivieUI.page_header(
        "Shopping Cart",
        "Your cart is currently empty",
        "🛒"
    )
    
    st.markdown("""
    <div class='solivie-card' style='text-align: center; padding: 3rem 2rem;'>
        <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 2rem;'>
            🛒 Your Cart is Empty
        </h3>
        <p style='color: #9BA8A5; margin: 0 0 2rem 0; font-size: 1.1rem;'>
            Start adding rooms to begin your booking
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔍 SEARCH ROOMS", use_container_width=True, type="primary", key="empty_search"):
            st.switch_page("pages/4_🔍_Search_Rooms.py")
    with col2:
        if st.button("👤 MY PROFILE", use_container_width=True, type="secondary", key="empty_profile"):
            st.switch_page("pages/6_👤_My_Profile.py")
    with col3:
        if st.button("🏠 HOME", use_container_width=True, type="secondary", key="empty_home"):
            st.switch_page("app.py")
    st.stop()


# ============================================================================
# MAIN CHECKOUT INTERFACE
# ============================================================================

SolivieUI.page_header(
    "Shopping Cart & Checkout",
    f"{cart_count} room(s) • {format_currency(cart_total)}",
    "🛒"
)

# Initialize checkout stage
if 'checkout_stage' not in st.session_state:
    st.session_state.checkout_stage = 'cart'  # cart -> details -> payment -> success


# ===== PROGRESS INDICATOR =====
stages = ['🛒 Cart', '📋 Details', '💳 Payment', '✅ Confirm']
current_stage_idx = ['cart', 'details', 'payment', 'success'].index(st.session_state.checkout_stage)

col1, col2, col3, col4 = st.columns(4)
for idx, (col, stage) in enumerate(zip([col1, col2, col3, col4], stages)):
    with col:
        if idx < current_stage_idx:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1rem;
                        border-radius: 10px;
                        text-align: center;
                        border: 2px solid #6B8E7E;'>
                <p style='color: #6B8E7E; margin: 0; font-weight: 600;'>✅ {stage}</p>
            </div>
            """, unsafe_allow_html=True)
        elif idx == current_stage_idx:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                        padding: 1rem;
                        border-radius: 10px;
                        text-align: center;
                        border: 2px solid #C4935B;'>
                <p style='color: #C4935B; margin: 0; font-weight: 700;'>➡️ {stage}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1rem;
                        border-radius: 10px;
                        text-align: center;
                        border: 2px solid #3D4A47;'>
                <p style='color: #9BA8A5; margin: 0;'>⚪ {stage}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)


# ============================================================================
# STAGE 1: CART REVIEW
# ============================================================================

if st.session_state.checkout_stage == 'cart':
    
    # Cart Summary
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 2rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            📋 Cart Summary
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #7B9CA8;'>
            <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>🛏️ Total Rooms</p>
            <p style='color: #7B9CA8; margin: 0; font-size: 2rem; font-weight: 700;'>{cart_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #7B9CA8;'>
            <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>👥 Total Guests</p>
            <p style='color: #7B9CA8; margin: 0; font-size: 2rem; font-weight: 700;'>{total_guests}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        checkin_date = st.session_state.cart_check_in.strftime('%b %d, %Y') if st.session_state.cart_check_in else "N/A"
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #6B8E7E;'>
            <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>📅 Check-in</p>
            <p style='color: #6B8E7E; margin: 0; font-size: 1.2rem; font-weight: 700;'>{checkin_date}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        checkout_date = st.session_state.cart_check_out.strftime('%b %d, %Y') if st.session_state.cart_check_out else "N/A"
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    border: 2px solid #6B8E7E;'>
            <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>📅 Check-out</p>
            <p style='color: #6B8E7E; margin: 0; font-size: 1.2rem; font-weight: 700;'>{checkout_date}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Cart Items
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 1.5rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            🛏️ Rooms in Cart
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    for idx, item in enumerate(st.session_state.cart):
        st.markdown("<div class='solivie-card' style='margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"""
            <h4 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 1.5rem;'>
                🏨 Room {item['room_number']} - {item['room_type']}
            </h4>
            <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                <strong>👥 Capacity:</strong> {item['capacity']} guests | 
                <strong>📊 Guests:</strong> {item['num_guests']}
            </p>
            <p style='color: #9BA8A5; margin: 0.5rem 0;'>
                {item['description']}
            </p>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem;'>Per Night</p>
                <p style='color: #C4935B; margin: 0.5rem 0; font-size: 1.5rem; font-weight: 700;'>
                    {format_currency(item['base_price'])}
                </p>
                <p style='color: #9BA8A5; margin: 1rem 0 0 0; font-size: 0.9rem;'>
                    Total ({item['nights']} nights)
                </p>
                <p style='color: #6B8E7E; margin: 0.5rem 0; font-size: 1.3rem; font-weight: 700;'>
                    {format_currency(item['total_price'])}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
            if st.button("🗑️ REMOVE", key=f"remove_{item['room_id']}", use_container_width=True, type="secondary"):
                CartManager.remove_from_cart(st.session_state, item['room_id'])
                st.success("✅ Room removed from cart")
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Cart Total
    st.markdown("""
    <div class='solivie-card' style='margin: 2rem 0;'>
        <h3 style='color: #C4935B; margin: 0 0 1.5rem 0; font-size: 1.5rem;'>
            💰 Cart Total
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style='color: #F5F5F0; line-height: 2;'>
            <p>• <strong>Number of Rooms:</strong> {cart_count}</p>
            <p>• <strong>Total Guests:</strong> {total_guests}</p>
            <p>• <strong>Check-in:</strong> {format_datetime(st.session_state.cart_check_in)}</p>
            <p>• <strong>Check-out:</strong> {format_datetime(st.session_state.cart_check_out)}</p>
            <p>• <strong>Total Nights:</strong> {st.session_state.cart[0]['nights']} per room</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                    padding: 2rem;
                    border-radius: 15px;
                    text-align: center;
                    border: 3px solid #C4935B;'>
            <p style='color: #9BA8A5; margin: 0 0 0.5rem 0; font-size: 1rem;'>
                Total for all rooms
            </p>
            <p style='color: #C4935B; margin: 0; font-size: 2.5rem; font-weight: 700;'>
                {format_currency(cart_total)}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Actions
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔍 CONTINUE SHOPPING", use_container_width=True, type="secondary", key="continue_shop"):
            st.switch_page("pages/4_🔍_Search_Rooms.py")
    
    with col2:
        if st.button("🗑️ CLEAR CART", use_container_width=True, type="secondary", key="clear_cart"):
            CartManager.clear_cart(st.session_state)
            st.success("✅ Cart cleared!")
            st.rerun()
    
    with col3:
        if st.button("➡️ PROCEED TO CHECKOUT", use_container_width=True, type="primary", key="proceed_checkout"):
            st.session_state.checkout_stage = 'details'
            st.rerun()


# ============================================================================
# STAGE 2: GUEST DETAILS & SPECIAL REQUESTS
# ============================================================================

elif st.session_state.checkout_stage == 'details':
    
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 2rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            👤 Guest Information
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        guest_name = st.text_input(
            "Full Name *",
            value=f"{user['first_name']} {user['last_name']}",
            key="guest_name_input"
        )
        guest_email = st.text_input(
            "Email *",
            value=user['email'],
            key="guest_email_input"
        )
    
    with col2:
        guest_phone = st.text_input(
            "Phone Number *",
            value=user.get('phone', ''),
            key="guest_phone_input",
            placeholder="+1 (555) 123-4567"
        )
        st.markdown("")
        st.caption("📧 Confirmation will be sent to this email")
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Special Requests
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 1.5rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            💬 Special Requests
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    special_requests = st.text_area(
        "Any special requirements or requests?",
        height=100,
        key="special_requests_input",
        placeholder="E.g., High floor, quiet room, early check-in, extra pillows..."
    )
    
    st.caption("💡 We'll do our best to accommodate your requests (subject to availability)")
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Per-Room Special Requests (Optional)
    if cart_count > 1:
        with st.expander("🛏️ Per-Room Special Requests (Optional)"):
            for idx, item in enumerate(st.session_state.cart):
                st.markdown(f"**Room {item['room_number']} - {item['room_type']}:**")
                room_request = st.text_input(
                    f"Special request for Room {item['room_number']}",
                    key=f"room_request_{item['room_id']}",
                    placeholder="Optional - specific request for this room only"
                )
                st.markdown("")
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Promo Code
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 1.5rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            🎁 Promo Code
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        promo_code = st.text_input(
            "Enter promo code (optional)",
            key="promo_code_input",
            placeholder="WELCOME10"
        )
    
    with col2:
        st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
        if st.button("✅ APPLY CODE", use_container_width=True, type="secondary", key="apply_promo"):
            if promo_code:
                # Simulate promo code validation
                valid_codes = {
                    "WELCOME10": 0.10,
                    "SUMMER2025": 0.15,
                    "LUXURY20": 0.20
                }
                
                if promo_code.upper() in valid_codes:
                    discount = valid_codes[promo_code.upper()]
                    st.session_state.discount_percent = discount
                    st.session_state.promo_code = promo_code.upper()
                    st.success(f"✅ {int(discount*100)}% discount applied!")
                    st.rerun()
                else:
                    st.error("❌ Invalid promo code")
            else:
                st.warning("⚠️ Please enter a code")
    
    # Show discount if applied
    if st.session_state.get('discount_percent'):
        discount_amount = cart_total * st.session_state.discount_percent
        new_total = cart_total - discount_amount
        
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    border: 2px solid #6B8E7E;
                    margin: 1rem 0;'>
            <p style='color: #6B8E7E; margin: 0 0 1rem 0; font-weight: 700;'>
                🎉 Promo code {st.session_state.promo_code} applied!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Total", format_currency(cart_total))
        with col2:
            st.metric("Discount", f"-{format_currency(discount_amount)}")
        with col3:
            st.metric("New Total", format_currency(new_total), delta=f"-{int(st.session_state.discount_percent*100)}%")
    
    st.caption("💡 Available codes: WELCOME10 (10% off), SUMMER2025 (15% off), LUXURY20 (20% off)")
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ BACK TO CART", use_container_width=True, type="secondary", key="back_to_cart"):
            st.session_state.checkout_stage = 'cart'
            st.rerun()
    
    with col2:
        if st.button("➡️ CONTINUE TO PAYMENT", use_container_width=True, type="primary", key="to_payment"):
            # Validation
            if not all([guest_name, guest_email, guest_phone]):
                st.error("❌ Please fill in all required fields")
            else:
                # Save guest details
                st.session_state.guest_details = {
                    'name': guest_name,
                    'email': guest_email,
                    'phone': guest_phone,
                    'special_requests': special_requests
                }
                st.session_state.checkout_stage = 'payment'
                st.rerun()


# ============================================================================
# STAGE 3: PAYMENT
# ============================================================================

elif st.session_state.checkout_stage == 'payment':
    
    # Calculate final total
    final_total = cart_total
    discount_amount = 0
    if st.session_state.get('discount_percent'):
        discount_amount = cart_total * st.session_state.discount_percent
        final_total = cart_total - discount_amount
    
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 2rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            💳 Payment Information
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Payment Method
    payment_method = st.selectbox(
        "Payment Method *",
        ["Credit Card", "Debit Card", "PayPal", "Bank Transfer"],
        key="payment_method_select"
    )
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Card Details (if card payment)
    if payment_method in ["Credit Card", "Debit Card"]:
        st.markdown("""
        <div style='padding: 1rem 0;'>
            <h4 style='color: #C4935B; margin: 0 0 1rem 0;'>💳 Card Details</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            card_number = st.text_input(
                "Card Number *",
                type="password",
                key="card_number_input",
                placeholder="4532 0151 1283 0366"
            )
            card_name = st.text_input(
                "Cardholder Name *",
                key="card_name_input",
                placeholder="John Doe"
            )
        
        with col2:
            card_expiry = st.text_input(
                "Expiry Date (MM/YY) *",
                key="card_expiry_input",
                placeholder="12/28"
            )
            card_cvv = st.text_input(
                "CVV *",
                type="password",
                key="card_cvv_input",
                max_chars=4,
                placeholder="123"
            )
        
        st.caption("🔒 Your payment information is secure and encrypted")
        st.info("💡 **Test Card:** 4532015112830366 | Expiry: 12/28 | CVV: 123")
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Booking Summary
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 1.5rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            📋 Booking Summary
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style='color: #F5F5F0; line-height: 2;'>
            <p><strong>Guest:</strong> {st.session_state.guest_details['name']}</p>
            <p><strong>Email:</strong> {st.session_state.guest_details['email']}</p>
            <p><strong>Phone:</strong> {st.session_state.guest_details['phone']}</p>
            <hr style='border-color: #3D4A47; margin: 1rem 0;'>
            <p><strong>Rooms:</strong> {cart_count}</p>
            <p><strong>Guests:</strong> {total_guests}</p>
            <p><strong>Check-in:</strong> {format_datetime(st.session_state.cart_check_in)}</p>
            <p><strong>Check-out:</strong> {format_datetime(st.session_state.cart_check_out)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.guest_details.get('special_requests'):
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1rem;
                        border-radius: 10px;
                        border: 2px solid #7B9CA8;
                        margin-top: 1rem;'>
                <p style='color: #7B9CA8; margin: 0 0 0.5rem 0; font-weight: 600;'>Special Requests:</p>
                <p style='color: #9BA8A5; margin: 0;'>{st.session_state.guest_details['special_requests']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                    padding: 2rem;
                    border-radius: 15px;
                    border: 3px solid #C4935B;'>
            <h4 style='color: #C4935B; margin: 0 0 1rem 0; text-align: center;'>
                💰 Amount Breakdown
            </h4>
            <p style='color: #F5F5F0; margin: 0.5rem 0;'>
                <strong>Subtotal:</strong> {format_currency(cart_total)}
            </p>
        """, unsafe_allow_html=True)
        
        if st.session_state.get('discount_percent'):
            st.markdown(f"""
            <p style='color: #6B8E7E; margin: 0.5rem 0;'>
                <strong>Discount ({st.session_state.promo_code}):</strong> -{format_currency(discount_amount)}
            </p>
            <hr style='border-color: #C4935B; margin: 1rem 0;'>
            <p style='color: #C4935B; margin: 0; font-size: 2rem; font-weight: 700; text-align: center;'>
                {format_currency(final_total)}
            </p>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <hr style='border-color: #C4935B; margin: 1rem 0;'>
            <p style='color: #C4935B; margin: 0; font-size: 2rem; font-weight: 700; text-align: center;'>
                {format_currency(cart_total)}
            </p>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.9rem; text-align: center;'>
                Total Amount
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Terms & Conditions
    agree_terms = st.checkbox(
        "✅ I agree to the Terms & Conditions and Cancellation Policy",
        key="agree_terms_checkbox"
    )
    
    st.caption("📄 [View Terms & Conditions](#) | [Cancellation Policy](#)")
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ BACK TO DETAILS", use_container_width=True, type="secondary", key="back_to_details"):
            st.session_state.checkout_stage = 'details'
            st.rerun()
    
    with col2:
        if st.button("🎉 CONFIRM & PAY", use_container_width=True, type="primary", key="confirm_pay"):
            # Validation
            if not agree_terms:
                st.error("❌ Please agree to Terms & Conditions")
            elif payment_method in ["Credit Card", "Debit Card"]:
                if not all([card_number, card_name, card_expiry, card_cvv]):
                    st.error("❌ Please fill in all card details")
                else:
                    # Process booking
                    st.session_state.processing = True
                    st.rerun()
            else:
                st.session_state.processing = True
                st.rerun()


# ============================================================================
# PROCESSING & SUCCESS
# ============================================================================

if st.session_state.get('processing'):
    
    st.markdown("""
    <div class='solivie-card' style='text-align: center; padding: 3rem 2rem;'>
        <h3 style='color: #C4935B; margin: 0 0 1rem 0; font-size: 2rem;'>
            ⏳ Processing Your Booking...
        </h3>
        <p style='color: #9BA8A5; margin: 0;'>
            Please wait while we confirm your reservation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    import time
    
    # Calculate final total
    final_total = cart_total
    if st.session_state.get('discount_percent'):
        discount_amount = cart_total * st.session_state.discount_percent
        final_total = cart_total - discount_amount
    
    booking_refs = []
    all_success = True
    
    for idx, item in enumerate(st.session_state.cart):
        progress = (idx + 1) / len(st.session_state.cart)
        progress_bar.progress(progress)
        status_text.text(f"Booking Room {item['room_number']}... ({idx + 1}/{len(st.session_state.cart)})")
        
        time.sleep(0.5)  # Simulate processing
        
        try:
            # Get per-room special request if exists
            room_special_request = st.session_state.get(f"room_request_{item['room_id']}", "")
            combined_requests = st.session_state.guest_details['special_requests']
            if room_special_request:
                combined_requests += f"\n[Room {item['room_number']}]: {room_special_request}"
            
            # Create booking
            success, booking_id, message = BookingManager.create_booking(
                st.session_state.user_id,
                item['room_id'],
                st.session_state.cart_check_in,
                st.session_state.cart_check_out,
                item['num_guests'],
                combined_requests,
                st.session_state.get('promo_code', '')
            )
            
            if not success:
                st.error(f"❌ Failed to book Room {item['room_number']}: {message}")
                all_success = False
                break
            
            # Process payment
            room_price = item['total_price']
            if st.session_state.get('discount_percent'):
                room_price = room_price * (1 - st.session_state.discount_percent)
            
            payment_success, payment_msg = PaymentProcessor.process_payment(
                booking_id,
                room_price,
                st.session_state.get('payment_method_select', 'Credit Card')
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
                    booking_refs.append({
                        'reference': booking_obj.booking_reference,
                        'room_number': item['room_number'],
                        'room_type': item['room_type'],
                        'price': room_price
                    })
        
        except Exception as e:
            st.error(f"❌ ERROR processing Room {item['room_number']}: {str(e)}")
            all_success = False
            break
    
    progress_bar.progress(1.0)
    status_text.text("✅ Complete!")
    
    if all_success:
        # Success!
        st.session_state.booking_refs = booking_refs
        st.session_state.checkout_stage = 'success'
        st.session_state.processing = False
        
        # Clear cart
        CartManager.clear_cart(st.session_state)
        
        # Clear checkout data
        if 'discount_percent' in st.session_state:
            del st.session_state.discount_percent
        if 'promo_code' in st.session_state:
            del st.session_state.promo_code
        if 'guest_details' in st.session_state:
            del st.session_state.guest_details
        
        st.rerun()
    else:
        st.error("⚠️ Some bookings failed. Please contact support.")
        st.session_state.processing = False


# ============================================================================
# STAGE 4: SUCCESS
# ============================================================================

elif st.session_state.checkout_stage == 'success':
    
    st.balloons()
    
    st.markdown("""
    <div class='solivie-card' style='text-align: center; padding: 3rem 2rem; margin-bottom: 2rem;'>
        <h1 style='color: #6B8E7E; margin: 0 0 1rem 0; font-size: 3rem;'>
            🎉 Booking Confirmed!
        </h1>
        <p style='color: #9BA8A5; margin: 0; font-size: 1.3rem;'>
            Your reservation has been successfully completed!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Booking References
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 2rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            📋 Your Booking References
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    for booking in st.session_state.booking_refs:
        st.markdown("<div class='solivie-card' style='margin-bottom: 1rem;'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            <h4 style='color: #C4935B; margin: 0 0 1rem 0;'>
                🏨 Room {booking['room_number']} - {booking['room_type']}
            </h4>
            """, unsafe_allow_html=True)
            st.code(booking['reference'], language=None)
        
        with col2:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem 0;'>
                <p style='color: #9BA8A5; margin: 0; font-size: 0.9rem;'>Amount Paid</p>
                <p style='color: #6B8E7E; margin: 0.5rem 0; font-size: 1.5rem; font-weight: 700;'>
                    {format_currency(booking['price'])}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Confirmation Details
    checkin_formatted = format_datetime(st.session_state.cart_check_in) if hasattr(st.session_state, 'cart_check_in') else "Your check-in date"
    
    st.markdown(f"""
    <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                padding: 2rem;
                border-radius: 15px;
                border: 2px solid #7B9CA8;
                margin: 2rem 0;'>
        <p style='color: #F5F5F0; margin: 0 0 1rem 0; font-size: 1.1rem;'>
            📧 <strong>Confirmation emails have been sent to:</strong> {st.session_state.guest_details.get('email', 'your email')}
        </p>
        <hr style='border-color: #3D4A47; margin: 1.5rem 0;'>
        <p style='color: #C4935B; margin: 0 0 1rem 0; font-weight: 700;'>💡 Next Steps:</p>
        <ul style='color: #9BA8A5; line-height: 2;'>
            <li>Check your email for booking confirmations</li>
            <li>Save your booking references</li>
            <li>Arrive on {checkin_formatted} for check-in</li>
        </ul>
        <hr style='border-color: #3D4A47; margin: 1.5rem 0;'>
        <p style='color: #9BA8A5; margin: 0;'>
            📞 <strong>Need Help?</strong> Contact us at 
            <span style='color: #C4935B;'>support@soliviehotel.com</span> or call 
            <span style='color: #C4935B;'>+1 (555) 123-4567</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Download Receipt (Placeholder)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 DOWNLOAD RECEIPT", use_container_width=True, type="secondary", key="download_receipt"):
            st.info("📄 Receipt download feature coming soon!")
    
    with col2:
        if st.button("📋 VIEW MY BOOKINGS", use_container_width=True, type="primary", key="view_bookings"):
            # Clear success state
            if 'booking_refs' in st.session_state:
                del st.session_state.booking_refs
            st.session_state.checkout_stage = 'cart'
            st.switch_page("pages/6_👤_My_Profile.py")
    
    with col3:
        if st.button("🏠 BACK TO HOME", use_container_width=True, type="secondary", key="success_home"):
            # Clear success state
            if 'booking_refs' in st.session_state:
                del st.session_state.booking_refs
            st.session_state.checkout_stage = 'cart'
            st.switch_page("app.py")


# ============================================================================
# FOOTER
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

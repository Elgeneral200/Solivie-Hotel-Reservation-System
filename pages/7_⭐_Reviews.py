"""
Reviews page.
Leave and view customer reviews.
"""

import streamlit as st
from backend.user.review_manager import ReviewManager
from backend.booking.booking_manager import BookingManager
from database.db_manager import get_db_session
from database.models import User, Room, Booking, Review
from utils.helpers import get_star_rating_display
from utils.constants import BookingStatus
import config

st.set_page_config(page_title="Reviews", page_icon="⭐", layout="wide")

st.title("⭐ Reviews & Ratings")

tab1, tab2 = st.tabs(["📝 Leave Review", "👀 View Reviews"])

# Leave review
with tab1:
    if not st.session_state.get('logged_in'):
        st.warning("Please login to leave a review")
        if st.button("🔐 Login"):
            st.switch_page("pages/2_🔐_Login.py")
    else:
        # Get completed bookings without reviews
        with get_db_session() as session:
            completed_bookings = session.query(Booking).filter(
                Booking.user_id == st.session_state.user_id,
                Booking.booking_status == BookingStatus.COMPLETED
            ).all()
            
            # Filter out bookings that already have reviews
            bookings_without_reviews = []
            for booking in completed_bookings:
                existing_review = session.query(Review).filter_by(
                    booking_id=booking.booking_id
                ).first()
                if not existing_review:
                    bookings_without_reviews.append(booking)
        
        if not bookings_without_reviews:
            st.info("📭 No completed bookings available for review")
        else:
            with st.form("review_form"):
                # Get room details for each booking
                booking_options = {}
                for b in bookings_without_reviews:
                    with get_db_session() as session:
                        room = session.query(Room).filter_by(room_id=b.room_id).first()
                    booking_options[f"Booking {b.booking_reference} - Room {room.room_number}"] = b.booking_id
                
                selected = st.selectbox("Select Booking", list(booking_options.keys()))
                booking_id = booking_options[selected]
                
                st.markdown("#### Rate Your Experience")
                rating = st.slider("Rating", 1, 5, 5, help="1 = Poor, 5 = Excellent")
                st.write(get_star_rating_display(rating))
                
                comment = st.text_area(
                    "Your Review",
                    placeholder="Share your experience...",
                    height=150
                )
                
                if st.form_submit_button("📮 Submit Review", use_container_width=True, type="primary"):
                    if not comment:
                        st.error("Please write a review")
                    else:
                        # Get booking details
                        with get_db_session() as session:
                            booking = session.query(Booking).filter_by(booking_id=booking_id).first()
                        
                        success, message = ReviewManager.create_review(
                            st.session_state.user_id,
                            booking.room_id,
                            booking_id,
                            rating,
                            comment
                        )
                        
                        if success:
                            st.success(message)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(message)

# View reviews
with tab2:
    st.markdown("### 👀 Guest Reviews")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        room_type_filter = st.selectbox("Filter by Room Type", ["All"] + list(config.ROOM_TYPES.keys()))
    with col2:
        sort_by = st.selectbox("Sort by", ["Newest First", "Highest Rating", "Lowest Rating"])
    
    # Get reviews
    with get_db_session() as session:
        query = session.query(Review).filter_by(status='approved')
        
        if room_type_filter != "All":
            query = query.join(Room).filter(Room.room_type == room_type_filter)
        
        if sort_by == "Newest First":
            query = query.order_by(Review.review_date.desc())
        elif sort_by == "Highest Rating":
            query = query.order_by(Review.rating.desc())
        elif sort_by == "Lowest Rating":
            query = query.order_by(Review.rating.asc())
        
        reviews = query.all()
    
    if not reviews:
        st.info("📭 No reviews yet. Be the first to leave one!")
    else:
        # Calculate average rating
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
        
        st.markdown(f"""
        <div style="background: #FFF3E0; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
            <h2>Overall Rating</h2>
            <h1 style="color: #FF9800; font-size: 3rem; margin: 0;">{avg_rating:.1f}/5.0</h1>
            <p style="font-size: 1.5rem; margin: 0.5rem 0;">{get_star_rating_display(int(round(avg_rating)))}</p>
            <p>Based on {len(reviews)} review(s)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display reviews
        for review in reviews:
            with get_db_session() as session:
                user = session.query(User).filter_by(user_id=review.user_id).first()
                room = session.query(Room).filter_by(room_id=review.room_id).first()
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1.5rem; margin: 1rem 0; background: white;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <h4 style="margin: 0;">👤 {user.first_name} {user.last_name[0]}.</h4>
                        <p style="color: #666; font-size: 0.9rem; margin: 0;">Room {room.room_number} - {room.room_type}</p>
                    </div>
                    <div style="font-size: 1.3rem;">
                        {get_star_rating_display(review.rating)}
                    </div>
                </div>
                <p style="margin: 1rem 0;">{review.comment}</p>
                <p style="color: #999; font-size: 0.85rem; margin: 0;">
                    {review.review_date.strftime('%B %d, %Y')}
                </p>
            </div>
            """, unsafe_allow_html=True)

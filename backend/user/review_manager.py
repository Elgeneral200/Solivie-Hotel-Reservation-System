"""
Review and rating management.
Handles customer reviews for rooms and stays.
"""

from database.db_manager import get_db_session
from database.models import Review, Booking
from datetime import datetime


class ReviewManager:
    """Manages reviews and ratings."""
    
    @staticmethod
    def create_review(user_id, room_id, booking_id, rating, comment):
        """Create new review."""
        try:
            with get_db_session() as session:
                # Check if review already exists
                existing = session.query(Review).filter_by(booking_id=booking_id).first()
                if existing:
                    return False, "Review already exists for this booking"
                
                # Verify booking is completed
                booking = session.query(Booking).filter_by(booking_id=booking_id).first()
                if not booking or booking.booking_status != 'completed':
                    return False, "Can only review completed bookings"
                
                new_review = Review(
                    user_id=user_id,
                    room_id=room_id,
                    booking_id=booking_id,
                    rating=rating,
                    comment=comment,
                    status='approved'
                )
                
                session.add(new_review)
                session.commit()
                
                return True, "Review submitted successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_room_reviews(room_id, status='approved'):
        """Get all reviews for a room."""
        try:
            with get_db_session() as session:
                return session.query(Review).filter_by(room_id=room_id, status=status).all()
        except:
            return []
    
    @staticmethod
    def get_average_rating(room_id):
        """Calculate average rating for room."""
        try:
            reviews = ReviewManager.get_room_reviews(room_id)
            if not reviews:
                return 0.0
            
            total = sum(r.rating for r in reviews)
            return round(total / len(reviews), 1)
        except:
            return 0.0
    
    @staticmethod
    def moderate_review(review_id, action, admin_response=None):
        """Moderate review (approve/reject/respond)."""
        try:
            with get_db_session() as session:
                review = session.query(Review).filter_by(review_id=review_id).first()
                if not review:
                    return False, "Review not found"
                
                if action in ['approved', 'rejected']:
                    review.status = action
                
                if admin_response:
                    review.admin_response = admin_response
                
                session.commit()
                return True, f"Review {action}"
        except Exception as e:
            return False, str(e)

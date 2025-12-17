"""
User profile management.
Handles user data and profile updates.
UPDATED: Added ID fields to user profile
"""

from database.db_manager import get_db_session
from database.models import User, Booking
from datetime import datetime


class UserManager:
    """Manages user profiles."""
    
    @staticmethod
    def get_user_profile(user_id):
        """
        Get complete user profile.
        Returns a dictionary to avoid session issues.
        UPDATED: Now includes ID information
        """
        try:
            with get_db_session() as session:
                user = session.query(User).filter_by(user_id=user_id).first()
                if not user:
                    return None
                
                # Return dictionary instead of SQLAlchemy object
                return {
                    'user_id': user.user_id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone_number': user.phone_number,
                    'address': user.address,
                    'city': user.city,
                    'country': user.country,
                    # NEW: ID information
                    'national_id': user.national_id,
                    'passport_number': user.passport_number,
                    'nationality': user.nationality,
                    'date_of_birth': user.date_of_birth,
                    'id_expiry_date': user.id_expiry_date,
                    # Original fields
                    'loyalty_points': user.loyalty_points,
                    'account_status': user.account_status,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at
                }
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    @staticmethod
    def update_profile(user_id, first_name=None, last_name=None, phone_number=None, address=None, city=None, country=None):
        """Update user profile information."""
        try:
            with get_db_session() as session:
                user = session.query(User).filter_by(user_id=user_id).first()
                if not user:
                    return False, "User not found"
                
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name
                if phone_number:
                    user.phone_number = phone_number
                if address:
                    user.address = address
                if city:
                    user.city = city
                if country:
                    user.country = country
                
                user.updated_at = datetime.utcnow()
                session.commit()
                
                return True, "Profile updated successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_user_statistics(user_id):
        """
        Get user booking statistics.
        FIXED: Correctly counts active bookings (excluding cancelled)
        """
        try:
            with get_db_session() as session:
                user = session.query(User).filter_by(user_id=user_id).first()
                all_bookings = session.query(Booking).filter_by(user_id=user_id).all()
                
                # FIX: Separate bookings by status
                active_bookings = [b for b in all_bookings if b.booking_status in ['confirmed', 'pending']]
                completed_bookings = [b for b in all_bookings if b.booking_status == 'completed']
                cancelled_bookings = [b for b in all_bookings if b.booking_status == 'cancelled']
                
                # FIX: Total spent includes only confirmed and completed
                total_spent = sum(b.total_amount for b in all_bookings if b.booking_status in ['confirmed', 'completed'])
                
                stats = {
                    'total_bookings': len(active_bookings),  # ✅ FIXED: Only active bookings
                    'completed_bookings': len(completed_bookings),
                    'cancelled_bookings': len(cancelled_bookings),
                    'total_spent': total_spent,
                    'loyalty_points': user.loyalty_points if user else 0,
                    'account_age_days': (datetime.utcnow() - user.created_at).days if user else 0
                }
                
                return stats
        except Exception as e:
            print(f"Error getting user statistics: {e}")
            return {
                'total_bookings': 0,
                'completed_bookings': 0,
                'cancelled_bookings': 0,
                'total_spent': 0,
                'loyalty_points': 0,
                'account_age_days': 0
            }

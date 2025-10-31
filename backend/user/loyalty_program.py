"""
Loyalty points program logic.
Manages earning and redemption of loyalty points.
"""

from database.db_manager import get_db_session
from database.models import User
import config


class LoyaltyProgram:
    """Manages loyalty program."""
    
    @staticmethod
    def add_points(user_id, points):
        """Add loyalty points to user account."""
        try:
            with get_db_session() as session:
                user = session.query(User).filter_by(user_id=user_id).first()
                if not user:
                    return False, "User not found"
                
                user.loyalty_points += points
                session.commit()
                
                return True, f"Added {points} points"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def redeem_points(user_id, points):
        """Redeem loyalty points for discount."""
        try:
            with get_db_session() as session:
                user = session.query(User).filter_by(user_id=user_id).first()
                if not user:
                    return False, 0, "User not found"
                
                if user.loyalty_points < points:
                    return False, 0, "Insufficient points"
                
                user.loyalty_points -= points
                discount_amount = points / config.POINTS_TO_DOLLAR_RATE
                session.commit()
                
                return True, discount_amount, f"Redeemed {points} points for ${discount_amount}"
        except Exception as e:
            return False, 0, str(e)
    
    @staticmethod
    def calculate_points_earned(amount):
        """Calculate points earned from booking amount."""
        return int(amount * config.LOYALTY_POINTS_RATE)
    
    @staticmethod
    def get_points_balance(user_id):
        """Get current points balance."""
        try:
            with get_db_session() as session:
                user = session.query(User).filter_by(user_id=user_id).first()
                return user.loyalty_points if user else 0
        except:
            return 0

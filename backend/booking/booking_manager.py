"""
Booking CRUD operations.
Manages booking creation, updates, and cancellations.
"""

from database.db_manager import get_db_session, DatabaseManager
from database.models import Booking, Room, User, PromoCode
from datetime import datetime
import random
import string


class BookingManager:
    """Manages booking operations."""
    
    @staticmethod
    def generate_booking_reference():
        """Generate unique booking reference."""
        chars = string.ascii_uppercase + string.digits
        return "BK" + "".join(random.choices(chars, k=6))
    
    @staticmethod
    def create_booking(user_id, room_id, check_in, check_out, num_guests, special_requests="", promo_code=""):
        """Create new booking and return booking data as dictionary."""
        try:
            with get_db_session() as session:
                booking_ref = BookingManager.generate_booking_reference()
                
                from backend.booking.pricing_calculator import PricingCalculator
                
                # Get room within session
                room = session.query(Room).filter_by(room_id=room_id).first()
                
                if not room:
                    return False, None, "Room not found"
                
                # Calculate total price
                total = PricingCalculator.calculate_total_price(
                    room.base_price_per_night,
                    check_in,
                    check_out,
                    num_guests,
                    room.capacity
                )
                
                # Apply promo code (calculate discount but don't store promo_code in Booking)
                if promo_code:
                    promo = session.query(PromoCode).filter_by(code=promo_code, active=True).first()
                    if promo:
                        discount_amount = (total * promo.discount_percentage) / 100
                        total -= discount_amount
                
                # ✅ FIX: Only use fields that exist in Booking model
                booking = Booking(
                    user_id=user_id,
                    room_id=room_id,
                    booking_reference=booking_ref,
                    check_in_date=check_in,
                    check_out_date=check_out,
                    num_guests=num_guests,
                    total_amount=total,
                    special_requests=special_requests,
                    booking_status='confirmed'
                )
                
                session.add(booking)
                session.flush()
                booking_id = booking.booking_id
                session.commit()
                
                DatabaseManager.log_action(user_id, 'booking_create', f'Booking {booking_ref} created')
                
                return True, booking_id, f"Booking created! Ref: {booking_ref}"
                
        except Exception as e:
            return False, None, str(e)
    
    @staticmethod
    def get_booking(booking_id):
        """
        Get booking details as dictionary (not object).
        """
        try:
            with get_db_session() as session:
                booking = session.query(Booking).filter_by(booking_id=booking_id).first()
                if not booking:
                    return None
                
                # ✅ FIX: Return dictionary with existing fields only
                return {
                    'booking_id': booking.booking_id,
                    'booking_reference': booking.booking_reference,
                    'user_id': booking.user_id,
                    'room_id': booking.room_id,
                    'check_in_date': booking.check_in_date,
                    'check_out_date': booking.check_out_date,
                    'num_guests': booking.num_guests,
                    'total_amount': booking.total_amount,
                    'special_requests': booking.special_requests,
                    'booking_status': booking.booking_status,
                    'created_at': booking.created_at,
                    'updated_at': booking.updated_at
                }
        except Exception as e:
            print(f"Error getting booking: {e}")
            return None
    
    @staticmethod
    def get_user_bookings(user_id):
        """Get all bookings for a user as dictionaries."""
        try:
            with get_db_session() as session:
                bookings = session.query(Booking).filter_by(user_id=user_id).order_by(Booking.created_at.desc()).all()
                
                # ✅ FIX: Return dictionaries with existing fields
                result = []
                for booking in bookings:
                    result.append({
                        'booking_id': booking.booking_id,
                        'booking_reference': booking.booking_reference,
                        'room_id': booking.room_id,
                        'check_in_date': booking.check_in_date,
                        'check_out_date': booking.check_out_date,
                        'num_guests': booking.num_guests,
                        'total_amount': booking.total_amount,
                        'special_requests': booking.special_requests,
                        'booking_status': booking.booking_status,
                        'created_at': booking.created_at
                    })
                
                return result
        except Exception as e:
            print(f"Error getting user bookings: {e}")
            return []
    
    @staticmethod
    def cancel_booking(booking_id):
        """Cancel a booking and calculate refund."""
        try:
            with get_db_session() as session:
                booking = session.query(Booking).filter_by(booking_id=booking_id).first()
                if not booking:
                    return False, 0, "Booking not found"
                
                if booking.booking_status == 'cancelled':
                    return False, 0, "Booking already cancelled"
                
                # Calculate refund (80% if >24h before check-in, else 0%)
                from datetime import timedelta
                hours_until_checkin = (booking.check_in_date - datetime.utcnow()).total_seconds() / 3600
                
                if hours_until_checkin > 24:
                    refund = booking.total_amount * 0.80
                else:
                    refund = 0
                
                booking.booking_status = 'cancelled'
                session.commit()
                
                DatabaseManager.log_action(booking.user_id, 'booking_cancel', f'Booking {booking.booking_reference} cancelled')
                
                return True, refund, f"Booking cancelled! Refund: ${refund:.2f}"
                
        except Exception as e:
            return False, 0, str(e)

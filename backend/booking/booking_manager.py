"""
Booking CRUD operations.
Manages booking creation, updates, and cancellations.
Sends email notifications for bookings and cancellations.
"""

from database.db_manager import get_db_session, DatabaseManager
from database.models import Booking, Room, User, PromoCode
from datetime import datetime
import random
import string
import config


class BookingManager:
    """Manages booking operations with email notifications."""
    
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
                
                # Get user for email
                user = session.query(User).filter_by(user_id=user_id).first()
                if not user:
                    return False, None, "User not found"
                
                # Calculate total price
                total = PricingCalculator.calculate_total_price(
                    room.base_price_per_night,
                    check_in,
                    check_out,
                    num_guests,
                    room.capacity
                )
                
                # Apply promo code (calculate discount but don't store promo_code in Booking)
                discount_applied = 0
                if promo_code:
                    promo = session.query(PromoCode).filter_by(code=promo_code, active=True).first()
                    if promo:
                        discount_amount = (total * promo.discount_percentage) / 100
                        total -= discount_amount
                        discount_applied = discount_amount
                
                # Calculate number of nights
                nights = (check_out - check_in).days
                
                # Create booking
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
                
                # ✅ SEND CONFIRMATION EMAIL
                try:
                    from backend.notification.email_service import EmailService
                    
                    # Prepare booking data for email
                    booking_data = {
                        'guest_name': f"{user.first_name} {user.last_name}",
                        'booking_reference': booking_ref,
                        'room_type': room.room_type,
                        'room_number': room.room_number,
                        'check_in': check_in,
                        'check_out': check_out,
                        'num_guests': num_guests,
                        'total_amount': total,
                        'nights': nights
                    }
                    
                    # Send email (non-blocking - won't fail booking if email fails)
                    email_sent = EmailService.send_booking_confirmation(
                        to_email=user.email,
                        booking_data=booking_data
                    )
                    
                    if email_sent:
                        print(f"✅ Confirmation email sent to {user.email}")
                    else:
                        print(f"⚠️  Booking created but email failed for {user.email}")
                        
                except Exception as e:
                    # Email failure shouldn't break booking
                    print(f"⚠️  Email notification failed: {e}")
                    print("✅ Booking still created successfully")
                
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
    def get_booking_with_details(booking_id):
        """
        Get booking with user and room details for email notifications.
        """
        try:
            with get_db_session() as session:
                booking = session.query(Booking).filter_by(booking_id=booking_id).first()
                if not booking:
                    return None
                
                user = session.query(User).filter_by(user_id=booking.user_id).first()
                room = session.query(Room).filter_by(room_id=booking.room_id).first()
                
                return {
                    'booking': booking,
                    'user': user,
                    'room': room
                }
        except Exception as e:
            print(f"Error getting booking details: {e}")
            return None
    
    @staticmethod
    def get_user_bookings(user_id):
        """Get all bookings for a user as dictionaries."""
        try:
            with get_db_session() as session:
                bookings = session.query(Booking).filter_by(user_id=user_id).order_by(Booking.created_at.desc()).all()
                
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
        """Cancel a booking, calculate refund, and send cancellation email."""
        try:
            with get_db_session() as session:
                booking = session.query(Booking).filter_by(booking_id=booking_id).first()
                if not booking:
                    return False, 0, "Booking not found"
                
                if booking.booking_status == 'cancelled':
                    return False, 0, "Booking already cancelled"
                
                # Get user for email
                user = session.query(User).filter_by(user_id=booking.user_id).first()
                
                # Calculate refund (80% if >24h before check-in, else 0%)
                from datetime import timedelta
                hours_until_checkin = (booking.check_in_date - datetime.utcnow()).total_seconds() / 3600
                
                if hours_until_checkin > 24:
                    refund = booking.total_amount * 0.80
                else:
                    refund = 0
                
                # Store booking reference before updating
                booking_ref = booking.booking_reference
                
                # Update booking status
                booking.booking_status = 'cancelled'
                session.commit()
                
                DatabaseManager.log_action(booking.user_id, 'booking_cancel', f'Booking {booking_ref} cancelled')
                
                # ✅ SEND CANCELLATION EMAIL
                if user:
                    try:
                        from backend.notification.email_service import EmailService
                        
                        cancellation_data = {
                            'guest_name': f"{user.first_name} {user.last_name}",
                            'booking_reference': booking_ref,
                            'refund_amount': refund,
                            'cancellation_date': datetime.now()
                        }
                        
                        email_sent = EmailService.send_cancellation_notice(
                            to_email=user.email,
                            cancellation_data=cancellation_data
                        )
                        
                        if email_sent:
                            print(f"✅ Cancellation email sent to {user.email}")
                        else:
                            print(f"⚠️  Cancellation processed but email failed for {user.email}")
                            
                    except Exception as e:
                        print(f"⚠️  Cancellation email notification failed: {e}")
                
                return True, refund, f"Booking cancelled! Refund: {config.CURRENCY_SYMBOL}{refund:.2f}"
                
        except Exception as e:
            return False, 0, str(e)

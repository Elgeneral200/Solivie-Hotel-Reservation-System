"""
Payment processing logic.
Handles payment transactions and gateway integration.
Sends payment receipt emails.
"""

from database.db_manager import get_db_session
from database.models import Payment, Booking, User
from utils.helpers import generate_transaction_id
from datetime import datetime


class PaymentProcessor:
    """Processes payment transactions with email notifications."""
    
    @staticmethod
    def process_payment(booking_id, amount, payment_method, card_details=None):
        """
        Process payment for booking and send receipt email.
        Returns: (success: bool, message: str)
        """
        try:
            # Simulate payment gateway processing
            transaction_id = generate_transaction_id()
            
            # In production, integrate with real payment gateway here
            payment_successful = True  # Simulate success
            
            if payment_successful:
                with get_db_session() as session:
                    # Create payment record
                    payment = Payment(
                        booking_id=booking_id,
                        amount=amount,
                        payment_method=payment_method,
                        transaction_id=transaction_id,
                        payment_status='completed',
                        payment_date=datetime.utcnow()
                    )
                    session.add(payment)
                    
                    # Update booking status
                    booking = session.query(Booking).filter_by(booking_id=booking_id).first()
                    if booking:
                        booking.booking_status = 'confirmed'
                        
                        # Get user for email
                        user = session.query(User).filter_by(user_id=booking.user_id).first()
                        
                        # Store data for email (before committing)
                        booking_ref = booking.booking_reference
                        user_email = user.email if user else None
                        user_name = f"{user.first_name} {user.last_name}" if user else "Guest"
                    else:
                        booking_ref = None
                        user_email = None
                        user_name = "Guest"
                    
                    session.commit()
                
                # ✅ SEND PAYMENT RECEIPT EMAIL
                if user_email and booking_ref:
                    try:
                        from backend.notification.email_service import EmailService
                        
                        payment_data = {
                            'guest_name': user_name,
                            'booking_reference': booking_ref,
                            'amount': amount,
                            'payment_method': payment_method,
                            'transaction_id': transaction_id,
                            'payment_date': datetime.now()
                        }
                        
                        email_sent = EmailService.send_payment_receipt(
                            to_email=user_email,
                            payment_data=payment_data
                        )
                        
                        if email_sent:
                            print(f"✅ Payment receipt sent to {user_email}")
                        else:
                            print(f"⚠️  Payment processed but receipt email failed for {user_email}")
                            
                    except Exception as e:
                        # Email failure shouldn't break payment
                        print(f"⚠️  Payment receipt email notification failed: {e}")
                        print("✅ Payment still processed successfully")
                
                return True, f"Payment successful! Transaction ID: {transaction_id}"
            else:
                return False, "Payment declined"
                
        except Exception as e:
            return False, f"Payment failed: {str(e)}"
    
    @staticmethod
    def get_payment_by_booking(booking_id):
        """Get payment details for a booking."""
        try:
            with get_db_session() as session:
                payment = session.query(Payment).filter_by(booking_id=booking_id).first()
                if payment:
                    return {
                        'payment_id': payment.payment_id,
                        'booking_id': payment.booking_id,
                        'amount': payment.amount,
                        'payment_method': payment.payment_method,
                        'transaction_id': payment.transaction_id,
                        'payment_status': payment.payment_status,
                        'payment_date': payment.payment_date
                    }
                return None
        except Exception as e:
            print(f"Error getting payment: {e}")
            return None
    
    @staticmethod
    def get_payment_with_details(booking_id):
        """
        Get payment with booking and user details for email notifications.
        """
        try:
            with get_db_session() as session:
                payment = session.query(Payment).filter_by(booking_id=booking_id).first()
                if not payment:
                    return None
                
                booking = session.query(Booking).filter_by(booking_id=booking_id).first()
                user = session.query(User).filter_by(user_id=booking.user_id).first() if booking else None
                
                return {
                    'payment': payment,
                    'booking': booking,
                    'user': user
                }
        except Exception as e:
            print(f"Error getting payment details: {e}")
            return None
    
    @staticmethod
    def validate_card_number(card_number):
        """Validate card number using Luhn algorithm."""
        card_number = card_number.replace(' ', '').replace('-', '')
        
        if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            return False
        
        # Luhn algorithm
        def luhn_checksum(num):
            digits = [int(d) for d in str(num)]
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum([int(x) for x in str(d * 2)])
            return checksum % 10
        
        return luhn_checksum(card_number) == 0

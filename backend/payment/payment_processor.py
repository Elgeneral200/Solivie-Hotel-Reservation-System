"""
Payment processing logic.
Handles payment transactions and gateway integration.
"""

from database.db_manager import get_db_session
from database.models import Payment, Booking
from utils.helpers import generate_transaction_id
from datetime import datetime


class PaymentProcessor:
    """Processes payment transactions."""
    
    @staticmethod
    def process_payment(booking_id, amount, payment_method, card_details=None):
        """
        Process payment for booking.
        ✅ FIXED: Returns only 2 values: (success, message)
        """
        try:
            # Simulate payment gateway processing
            transaction_id = generate_transaction_id()
            
            # In production, integrate with real payment gateway here
            payment_successful = True  # Simulate success
            
            if payment_successful:
                with get_db_session() as session:
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
                    
                    session.commit()
                
                # ✅ FIX: Return only 2 values
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
                    # ✅ FIX: Return as dictionary to avoid session issues
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

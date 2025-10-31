"""
Refund processing logic.
Handles refund calculations and processing.
"""

from database.db_manager import get_db_session
from database.models import Payment
from datetime import datetime


class RefundManager:
    """Manages refund operations."""
    
    @staticmethod
    def process_refund(payment_id, refund_amount, reason):
        """
        Process refund for payment.
        Returns: (success, message)
        """
        try:
            with get_db_session() as session:
                payment = session.query(Payment).filter_by(payment_id=payment_id).first()
                
                if not payment:
                    return False, "Payment not found"
                
                if payment.payment_status == 'refunded':
                    return False, "Already refunded"
                
                # In production, integrate with payment gateway for actual refund
                refund_successful = True  # Simulate success
                
                if refund_successful:
                    if refund_amount >= payment.amount:
                        payment.payment_status = 'refunded'
                    else:
                        payment.payment_status = 'partial_refund'
                    
                    session.commit()
                    return True, f"Refund of {refund_amount} processed successfully"
                else:
                    return False, "Refund processing failed"
                    
        except Exception as e:
            return False, f"Refund failed: {str(e)}"
    
    @staticmethod
    def get_refund_status(payment_id):
        """Check refund status of payment."""
        try:
            with get_db_session() as session:
                payment = session.query(Payment).filter_by(payment_id=payment_id).first()
                if payment:
                    return payment.payment_status
                return None
        except:
            return None

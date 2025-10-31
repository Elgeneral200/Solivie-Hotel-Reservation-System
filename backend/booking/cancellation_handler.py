"""
Booking cancellation logic.
Handles cancellation policies and refund calculations.
"""

from datetime import datetime
import config


class CancellationHandler:
    """Handles booking cancellations."""
    
    @staticmethod
    def calculate_refund(booking, cancellation_time=None):
        """
        Calculate refund amount based on cancellation policy.
        Returns: (refund_amount, fee, can_cancel)
        """
        if cancellation_time is None:
            cancellation_time = datetime.now()
        
        hours_until_checkin = (booking.check_in_date - cancellation_time).total_seconds() / 3600
        
        if hours_until_checkin < 0:
            return 0, booking.total_amount, False
        
        if hours_until_checkin >= config.CANCELLATION_HOURS:
            return booking.total_amount, 0, True
        else:
            fee = booking.total_amount * (config.CANCELLATION_FEE_PERCENTAGE / 100)
            refund = booking.total_amount - fee
            return round(refund, 2), round(fee, 2), True
    
    @staticmethod
    def get_cancellation_policy_text():
        """Get human-readable cancellation policy."""
        return f"""
        Cancellation Policy:
        - Free cancellation up to {config.CANCELLATION_HOURS} hours before check-in
        - Cancellations within {config.CANCELLATION_HOURS} hours incur {config.CANCELLATION_FEE_PERCENTAGE}% fee
        - No refund for no-shows
        """

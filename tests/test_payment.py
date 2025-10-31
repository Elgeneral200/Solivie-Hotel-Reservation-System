"""
Tests for payment functionality.
"""

import unittest
from backend.payment.payment_processor import PaymentProcessor


class TestPayment(unittest.TestCase):
    """Test payment functions."""
    
    def test_card_validation(self):
        """Test credit card validation."""
        # Valid test card
        self.assertTrue(PaymentProcessor.validate_card_number("4532015112830366"))
        
        # Invalid card
        self.assertFalse(PaymentProcessor.validate_card_number("1234567890123456"))
        self.assertFalse(PaymentProcessor.validate_card_number("invalid"))


if __name__ == '__main__':
    unittest.main()

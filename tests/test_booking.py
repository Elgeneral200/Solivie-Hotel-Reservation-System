"""
Tests for booking functionality.
"""

import unittest
from datetime import datetime, timedelta
from backend.booking.pricing_calculator import PricingCalculator


class TestBooking(unittest.TestCase):
    """Test booking functions."""
    
    def test_pricing_calculation(self):
        """Test price calculation."""
        check_in = datetime.now() + timedelta(days=7)
        check_out = check_in + timedelta(days=3)
        
        price = PricingCalculator.calculate_total_price(
            base_price=100,
            check_in=check_in,
            check_out=check_out,
            num_guests=2,
            room_capacity=2
        )
        
        self.assertGreater(price, 0)
        self.assertIsInstance(price, float)
    
    def test_nights_calculation(self):
        """Test nights calculation."""
        from utils.helpers import calculate_nights
        
        check_in = datetime(2025, 11, 1)
        check_out = datetime(2025, 11, 5)
        
        nights = calculate_nights(check_in, check_out)
        self.assertEqual(nights, 4)


if __name__ == '__main__':
    unittest.main()

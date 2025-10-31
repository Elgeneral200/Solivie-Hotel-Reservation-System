"""
Dynamic pricing engine.
Calculates booking prices with seasonal rates, discounts, and surcharges.
"""

from datetime import datetime, timedelta
import config


class PricingCalculator:
    """Calculates booking prices."""
    
    @staticmethod
    def calculate_total_price(base_price, check_in, check_out, num_guests, room_capacity, promo_code=None):
        """Calculate total booking price with all factors."""
        num_nights = (check_out - check_in).days
        if num_nights <= 0:
            return 0.0
        
        total = base_price * num_nights
        
        # Weekend surcharge
        current = check_in
        while current < check_out:
            if current.weekday() in [4, 5]:
                total += base_price * (config.WEEKEND_SURCHARGE_PERCENTAGE / 100)
            current += timedelta(days=1)
        
        # Extra guest charge
        if num_guests > room_capacity:
            total += (num_guests - room_capacity) * config.EXTRA_GUEST_CHARGE_PER_NIGHT * num_nights
        
        # Seasonal pricing
        if check_in.month in config.PEAK_SEASON_MONTHS:
            total *= (1 + config.PEAK_SEASON_INCREASE / 100)
        
        # Long stay discount
        if num_nights >= 14:
            total *= (1 - config.LONG_STAY_DISCOUNT_14_DAYS / 100)
        elif num_nights >= 7:
            total *= (1 - config.LONG_STAY_DISCOUNT_7_DAYS / 100)
        
        # Promo code
        if promo_code:
            discount = PricingCalculator.apply_promo_code(promo_code, total)
            total -= discount
        
        # Tax
        total *= (1 + config.TAX_PERCENTAGE / 100)
        
        return round(total, 2)
    
    @staticmethod
    def apply_promo_code(code, amount):
        """Apply promotional discount."""
        from database.db_manager import get_db_session
        from database.models import PromoCode
        
        try:
            with get_db_session() as session:
                promo = session.query(PromoCode).filter_by(code=code.upper(), active=True).first()
                
                if not promo:
                    return 0
                
                now = datetime.now()
                if not (promo.valid_from <= now <= promo.valid_until):
                    return 0
                
                if promo.usage_limit and promo.times_used >= promo.usage_limit:
                    return 0
                
                discount = amount * (promo.discount_percentage / 100)
                promo.times_used += 1
                session.commit()
                
                return round(discount, 2)
        except:
            return 0
    
    @staticmethod
    def get_price_breakdown(base_price, check_in, check_out, num_guests, room_capacity):
        """Get itemized price breakdown."""
        num_nights = (check_out - check_in).days
        
        breakdown = {
            'base_price': base_price,
            'num_nights': num_nights,
            'subtotal': base_price * num_nights,
            'weekend_surcharge': 0,
            'extra_guest_charge': 0,
            'seasonal_adjustment': 0,
            'long_stay_discount': 0,
            'tax': 0,
            'total': 0
        }
        
        # Calculate each component
        current = check_in
        while current < check_out:
            if current.weekday() in [4, 5]:
                breakdown['weekend_surcharge'] += base_price * (config.WEEKEND_SURCHARGE_PERCENTAGE / 100)
            current += timedelta(days=1)
        
        if num_guests > room_capacity:
            breakdown['extra_guest_charge'] = (num_guests - room_capacity) * config.EXTRA_GUEST_CHARGE_PER_NIGHT * num_nights
        
        running = breakdown['subtotal'] + breakdown['weekend_surcharge'] + breakdown['extra_guest_charge']
        
        if check_in.month in config.PEAK_SEASON_MONTHS:
            breakdown['seasonal_adjustment'] = running * (config.PEAK_SEASON_INCREASE / 100)
            running += breakdown['seasonal_adjustment']
        
        if num_nights >= 14:
            breakdown['long_stay_discount'] = -running * (config.LONG_STAY_DISCOUNT_14_DAYS / 100)
        elif num_nights >= 7:
            breakdown['long_stay_discount'] = -running * (config.LONG_STAY_DISCOUNT_7_DAYS / 100)
        
        running += breakdown['long_stay_discount']
        breakdown['tax'] = running * (config.TAX_PERCENTAGE / 100)
        breakdown['total'] = round(running + breakdown['tax'], 2)
        
        return breakdown

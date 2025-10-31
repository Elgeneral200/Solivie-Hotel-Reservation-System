"""
Input validation functions.
Validates emails, passwords, phone numbers, dates, etc.
"""

import re
from datetime import datetime
import config


def validate_email(email):
    """Validate email format."""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password):
    """Check if password meets requirements."""
    if not password or len(password) < config.MIN_PASSWORD_LENGTH:
        return False
    
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    
    return has_upper and has_lower and has_digit


def validate_phone_number(phone):
    """Validate phone number format."""
    if not phone:
        return False
    cleaned = re.sub(r'[\s\-\.\(\)]', '', phone)
    return bool(re.match(r'^\+?\d{9,15}$', cleaned))


def validate_date_range(check_in, check_out):
    """
    Validate booking date range.
    Returns: (is_valid, error_message)
    """
    if not check_in or not check_out:
        return False, "Dates are required"
    
    if check_out <= check_in:
        return False, "Check-out must be after check-in"
    
    num_nights = (check_out - check_in).days
    
    if num_nights < config.MIN_BOOKING_DAYS:
        return False, f"Minimum stay is {config.MIN_BOOKING_DAYS} night(s)"
    
    if num_nights > config.MAX_BOOKING_DAYS:
        return False, f"Maximum stay is {config.MAX_BOOKING_DAYS} nights"
    
    if check_in < datetime.now():
        return False, "Check-in cannot be in the past"
    
    # Check maximum advance booking
    from datetime import timedelta
    max_advance = datetime.now() + timedelta(days=config.MAX_ADVANCE_BOOKING_DAYS)
    if check_in > max_advance:
        return False, f"Cannot book more than {config.MAX_ADVANCE_BOOKING_DAYS} days in advance"
    
    return True, "Valid date range"


def validate_guest_count(num_guests, room_capacity):
    """
    Validate number of guests.
    Returns: (is_valid, error_message)
    """
    if num_guests < 1:
        return False, "At least one guest required"
    
    if num_guests > room_capacity + 2:
        return False, f"Too many guests (max: {room_capacity + 2})"
    
    return True, "Valid guest count"


def sanitize_input(text, max_length=None):
    """Remove dangerous characters from input."""
    if not text:
        return ""
    
    text = str(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[;<>]', '', text)
    text = text.strip()
    
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_booking_reference(reference):
    """Validate booking reference format (BK + 6 alphanumeric)."""
    if not reference:
        return False
    pattern = r'^BK[A-Z0-9]{6}$'
    return bool(re.match(pattern, reference.upper()))


def validate_promo_code(code):
    """Validate promotional code format (6-20 alphanumeric)."""
    if not code:
        return False
    pattern = r'^[A-Z0-9]{6,20}$'
    return bool(re.match(pattern, code.upper()))

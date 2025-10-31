"""
Helper utility functions.
Common functions used throughout the application.
"""

import random
import string
from datetime import datetime
import config


def generate_booking_reference():
    """Generate unique booking reference code (BK + 6 chars)."""
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=6))
    return f"BK{random_part}"


def generate_transaction_id():
    """Generate unique transaction ID."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"TXN-{timestamp}-{random_part}"


def format_currency(amount):
    """Format amount as currency string."""
    return f"{config.CURRENCY_SYMBOL}{amount:,.2f}"


def format_date(date_obj):
    """Format date as string."""
    return date_obj.strftime(config.DATE_FORMAT)


def format_datetime(datetime_obj):
    """Format datetime as string."""
    return datetime_obj.strftime(config.DATETIME_FORMAT)


def calculate_nights(check_in, check_out):
    """Calculate number of nights between dates."""
    return (check_out - check_in).days


def get_star_rating_display(rating):
    """Convert numeric rating to star display."""
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return "☆☆☆☆☆"
    return "⭐" * rating + "☆" * (5 - rating)


def get_greeting():
    """Get time-appropriate greeting."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 22:
        return "Good Evening"
    else:
        return "Good Night"


def truncate_text(text, max_length=100):
    """Truncate text to max length."""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def get_percentage(part, whole):
    """Calculate percentage safely."""
    if whole == 0:
        return 0.0
    return round((part / whole) * 100, 2)


def mask_email(email):
    """Mask email for privacy (e.g., j***@example.com)."""
    if not email or '@' not in email:
        return email
    
    local, domain = email.split('@')
    if len(local) <= 3:
        masked_local = local[0] + '***'
    else:
        masked_local = local[0] + '***' + local[-1]
    
    return f"{masked_local}@{domain}"

"""
Application constants and enums.
Defines status constants and standard messages.
"""


class BookingStatus:
    """Booking status constants."""
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    CHECKED_IN = 'checked_in'
    CHECKED_OUT = 'checked_out'
    
    @classmethod
    def get_all(cls):
        return [cls.PENDING, cls.CONFIRMED, cls.CANCELLED, cls.COMPLETED, cls.CHECKED_IN, cls.CHECKED_OUT]


class PaymentStatus:
    """Payment status constants."""
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'
    
    @classmethod
    def get_all(cls):
        return [cls.PENDING, cls.COMPLETED, cls.FAILED, cls.REFUNDED]


class RoomStatus:
    """Room status constants."""
    AVAILABLE = 'available'
    OCCUPIED = 'occupied'
    MAINTENANCE = 'maintenance'
    CLEANING = 'cleaning'
    
    @classmethod
    def get_all(cls):
        return [cls.AVAILABLE, cls.OCCUPIED, cls.MAINTENANCE, cls.CLEANING]


class ErrorMessages:
    """Standard error messages."""
    INVALID_EMAIL = "Invalid email format"
    INVALID_PASSWORD = "Password must be at least 8 characters with uppercase, lowercase, and numbers"
    EMAIL_EXISTS = "Email already registered"
    USER_NOT_FOUND = "User not found"
    INVALID_CREDENTIALS = "Invalid credentials"
    ROOM_NOT_AVAILABLE = "Room not available"
    BOOKING_FAILED = "Booking failed"
    PAYMENT_FAILED = "Payment failed"


class SuccessMessages:
    """Standard success messages."""
    REGISTRATION_SUCCESS = "Registration successful"
    LOGIN_SUCCESS = "Login successful"
    BOOKING_SUCCESS = "Booking confirmed"
    PAYMENT_SUCCESS = "Payment successful"
    UPDATE_SUCCESS = "Updated successfully"

"""
SQLAlchemy ORM models for all database tables.
Defines User, Room, Booking, Payment, Review, AdminUser, PromoCode, and AuditLog.
UPDATED: Added National ID and Check-in/Check-out fields
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import config


Base = declarative_base()


class User(Base):
    """Customer user accounts."""
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone_number = Column(String(20))
    
    # NEW: National ID / Passport Information
    national_id = Column(String(50))
    passport_number = Column(String(50))
    nationality = Column(String(50))
    date_of_birth = Column(Date)
    id_expiry_date = Column(Date)
    
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    loyalty_points = Column(Integer, default=0)
    account_status = Column(String(20), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")


class Room(Base):
    """Hotel room inventory."""
    __tablename__ = 'rooms'
    
    room_id = Column(Integer, primary_key=True, autoincrement=True)
    room_number = Column(String(10), unique=True, nullable=False)
    room_type = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    base_price_per_night = Column(Float, nullable=False)
    description = Column(Text)
    amenities = Column(JSON)
    floor_number = Column(Integer)
    view_type = Column(String(50))
    status = Column(String(20), default='available')
    images = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="room", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="room", cascade="all, delete-orphan")


class Booking(Base):
    """Room reservations."""
    __tablename__ = 'bookings'
    
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    room_id = Column(Integer, ForeignKey('rooms.room_id'), nullable=False, index=True)
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    num_guests = Column(Integer, nullable=False)
    special_requests = Column(Text)
    total_amount = Column(Float, nullable=False)
    booking_status = Column(String(20), default='pending', index=True)
    booking_reference = Column(String(20), unique=True, nullable=False)
    
    # NEW: Check-in/Check-out Tracking (for Feature 3)
    actual_check_in = Column(DateTime)
    actual_check_out = Column(DateTime)
    checked_in_by = Column(Integer, ForeignKey('admin_users.admin_id'))
    checked_out_by = Column(Integer, ForeignKey('admin_users.admin_id'))
    
    # NEW: Guest ID Verification (for Feature 1)
    guest_id_number = Column(String(50))
    id_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False, cascade="all, delete-orphan")
    review = relationship("Review", back_populates="booking", uselist=False, cascade="all, delete-orphan")


class Payment(Base):
    """Payment transactions."""
    __tablename__ = 'payments'
    
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
    transaction_id = Column(String(100), unique=True)
    payment_status = Column(String(20), default='pending')
    payment_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    booking = relationship("Booking", back_populates="payment")


class Review(Base):
    """Customer reviews and ratings."""
    __tablename__ = 'reviews'
    
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    room_id = Column(Integer, ForeignKey('rooms.room_id'), nullable=False, index=True)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'), nullable=False, unique=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    review_date = Column(DateTime, default=datetime.utcnow)
    admin_response = Column(Text)
    status = Column(String(20), default='approved')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="reviews")
    room = relationship("Room", back_populates="reviews")
    booking = relationship("Booking", back_populates="review")


class AdminUser(Base):
    """Admin and staff accounts."""
    __tablename__ = 'admin_users'
    
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(200))
    email = Column(String(255), unique=True)
    role = Column(String(50), default='receptionist')
    permissions = Column(JSON)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class PromoCode(Base):
    """Promotional discount codes."""
    __tablename__ = 'promo_codes'
    
    promo_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    discount_percentage = Column(Float, nullable=False)
    valid_from = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    usage_limit = Column(Integer)
    times_used = Column(Integer, default=0)
    active = Column(Boolean, default=True)


class AuditLog(Base):
    """System activity audit trail."""
    __tablename__ = 'audit_logs'
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    action_type = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    ip_address = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


# Database engine and session
engine = create_engine(config.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_database():
    """Create all database tables."""
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")


def get_session():
    """Get a new database session."""
    return SessionLocal()

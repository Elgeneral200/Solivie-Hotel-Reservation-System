"""
Configuration settings for the Hotel Reservation System.
Centralizes all app settings, business rules, and constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# PATHS
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "hotel_system.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# ============================================================================
# SECURITY
# ============================================================================
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
SESSION_TIMEOUT = 3600

# Password requirements
MIN_PASSWORD_LENGTH = 8  # ✅ ADDED THIS
REQUIRE_UPPERCASE = True
REQUIRE_LOWERCASE = True
REQUIRE_NUMBERS = True
REQUIRE_SPECIAL_CHARS = False

# ============================================================================
# EMAIL
# ============================================================================
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@hotel.com")

# ============================================================================
# BUSINESS RULES
# ============================================================================
MIN_BOOKING_DAYS = 1
MAX_BOOKING_DAYS = 30
MAX_ADVANCE_BOOKING_DAYS = 365  # ✅ ADDED THIS
CANCELLATION_HOURS = 24
CANCELLATION_FEE_PERCENTAGE = 20
LOYALTY_POINTS_RATE = 10
POINTS_TO_DOLLAR_RATE = 100

# ============================================================================
# PRICING
# ============================================================================
WEEKEND_SURCHARGE_PERCENTAGE = 20
PEAK_SEASON_INCREASE = 30
LONG_STAY_DISCOUNT_7_DAYS = 10
LONG_STAY_DISCOUNT_14_DAYS = 15
EXTRA_GUEST_CHARGE_PER_NIGHT = 15
TAX_PERCENTAGE = 10
PEAK_SEASON_MONTHS = [6, 7, 8, 12]

# ============================================================================
# ROOM TYPES
# ============================================================================
ROOM_TYPES = {
    "Single": {
        "capacity": 1,
        "base_price": 50,
        "description": "Comfortable single room with essential amenities",
        "amenities": ["WiFi", "TV", "Air Conditioning", "Mini Fridge"]
    },
    "Double": {
        "capacity": 2,
        "base_price": 80,
        "description": "Spacious double room perfect for couples",
        "amenities": ["WiFi", "TV", "Air Conditioning", "Mini Fridge", "Coffee Maker"]
    },
    "Suite": {
        "capacity": 4,
        "base_price": 150,
        "description": "Luxurious suite with separate living area",
        "amenities": ["WiFi", "TV", "Air Conditioning", "Mini Fridge", "Coffee Maker", "Balcony", "Bathtub"]
    },
    "Deluxe": {
        "capacity": 2,
        "base_price": 200,
        "description": "Premium deluxe room with top-tier amenities",
        "amenities": ["WiFi", "TV", "Air Conditioning", "Mini Fridge", "Coffee Maker", "Balcony", "Bathtub", "Room Service"]
    }
}

# ============================================================================
# PAYMENT
# ============================================================================
PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Wallet"]

# ============================================================================
# APP METADATA
# ============================================================================
APP_NAME = "Hotel Reservation System"
APP_VERSION = "1.0.0"
COMPANY_NAME = "Solivie Hotel"
COMPANY_ADDRESS = "123 Hotel Street, City, Country"
COMPANY_PHONE = "+1 234 567 8900"
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@hotel.com")
CURRENCY_SYMBOL = "$"
CURRENCY_CODE = "USD"
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# ============================================================================
# FILE UPLOAD
# ============================================================================
MAX_FILE_SIZE_MB = 5
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
UPLOAD_FOLDER = BASE_DIR / "uploads"

# ============================================================================
# UI SETTINGS
# ============================================================================
ITEMS_PER_PAGE = 10

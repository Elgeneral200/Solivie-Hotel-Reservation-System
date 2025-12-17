"""
Database Migration Script
Adds National ID and Check-in/Check-out fields to existing database
"""
from database.models import engine
from sqlalchemy import text, inspect

def migrate():
    """Add new columns to existing tables."""
    print("🔄 Starting database migration...")
    
    with engine.connect() as conn:
        inspector = inspect(engine)
        
        try:
            # Check if columns already exist
            user_columns = [col['name'] for col in inspector.get_columns('users')]
            booking_columns = [col['name'] for col in inspector.get_columns('bookings')]
            
            # ===== USER TABLE MIGRATIONS =====
            print("📋 Checking users table...")
            
            if 'national_id' not in user_columns:
                conn.execute(text("ALTER TABLE users ADD COLUMN national_id VARCHAR(50)"))
                print("  ✅ Added: national_id")
            
            if 'passport_number' not in user_columns:
                conn.execute(text("ALTER TABLE users ADD COLUMN passport_number VARCHAR(50)"))
                print("  ✅ Added: passport_number")
            
            if 'nationality' not in user_columns:
                conn.execute(text("ALTER TABLE users ADD COLUMN nationality VARCHAR(50)"))
                print("  ✅ Added: nationality")
            
            if 'date_of_birth' not in user_columns:
                conn.execute(text("ALTER TABLE users ADD COLUMN date_of_birth DATE"))
                print("  ✅ Added: date_of_birth")
            
            if 'id_expiry_date' not in user_columns:
                conn.execute(text("ALTER TABLE users ADD COLUMN id_expiry_date DATE"))
                print("  ✅ Added: id_expiry_date")
            
            # ===== BOOKING TABLE MIGRATIONS =====
            print("\n📋 Checking bookings table...")
            
            if 'actual_check_in' not in booking_columns:
                conn.execute(text("ALTER TABLE bookings ADD COLUMN actual_check_in DATETIME"))
                print("  ✅ Added: actual_check_in")
            
            if 'actual_check_out' not in booking_columns:
                conn.execute(text("ALTER TABLE bookings ADD COLUMN actual_check_out DATETIME"))
                print("  ✅ Added: actual_check_out")
            
            if 'checked_in_by' not in booking_columns:
                conn.execute(text("ALTER TABLE bookings ADD COLUMN checked_in_by INTEGER"))
                print("  ✅ Added: checked_in_by")
            
            if 'checked_out_by' not in booking_columns:
                conn.execute(text("ALTER TABLE bookings ADD COLUMN checked_out_by INTEGER"))
                print("  ✅ Added: checked_out_by")
            
            if 'guest_id_number' not in booking_columns:
                conn.execute(text("ALTER TABLE bookings ADD COLUMN guest_id_number VARCHAR(50)"))
                print("  ✅ Added: guest_id_number")
            
            if 'id_verified' not in booking_columns:
                conn.execute(text("ALTER TABLE bookings ADD COLUMN id_verified BOOLEAN DEFAULT 0"))
                print("  ✅ Added: id_verified")
            
            if 'verification_date' not in booking_columns:
                conn.execute(text("ALTER TABLE bookings ADD COLUMN verification_date DATETIME"))
                print("  ✅ Added: verification_date")
            
            conn.commit()
            print("\n✅ Migration completed successfully!")
            print("🎉 Database is ready for Feature 1!")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            conn.rollback()

if __name__ == "__main__":
    migrate()

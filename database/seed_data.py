"""
Seed database with sample data for testing.
Run: python -m database.seed_data
"""

from database.models import init_database, get_session, Room, User, AdminUser, PromoCode
from backend.auth.authentication import AuthenticationManager
from datetime import datetime, timedelta
import random
import config


def seed_rooms():
    """Create sample rooms."""
    print("Seeding rooms...")
    session = get_session()
    
    rooms_data = []
    room_number = 101
    
    for floor in range(1, 6):
        for room_type, details in config.ROOM_TYPES.items():
            for i in range(2):
                room = Room(
                    room_number=str(room_number),
                    room_type=room_type,
                    capacity=details['capacity'],
                    base_price_per_night=details['base_price'],
                    description=details['description'],
                    amenities=details['amenities'],
                    floor_number=floor,
                    view_type=random.choice(['City', 'Garden', 'Sea']),
                    status='available',
                    images=[]
                )
                rooms_data.append(room)
                room_number += 1
    
    session.bulk_save_objects(rooms_data)
    session.commit()
    session.close()
    print(f"✅ Created {len(rooms_data)} rooms")


def seed_admin_users():
    """Create admin accounts."""
    print("Seeding admin users...")
    session = get_session()
    
    admins = [
        {
            'username': 'admin',
            'password': 'admin123',
            'full_name': 'System Administrator',
            'email': 'admin@hotel.com',
            'role': 'admin',
            'permissions': {'all': True}
        },
        {
            'username': 'manager',
            'password': 'manager123',
            'full_name': 'Hotel Manager',
            'email': 'manager@hotel.com',
            'role': 'manager',
            'permissions': {'view_bookings': True, 'edit_bookings': True, 'view_rooms': True}
        }
    ]
    
    for admin_data in admins:
        admin = AdminUser(
            username=admin_data['username'],
            password_hash=AuthenticationManager.hash_password(admin_data['password']),
            full_name=admin_data['full_name'],
            email=admin_data['email'],
            role=admin_data['role'],
            permissions=admin_data['permissions']
        )
        session.add(admin)
    
    session.commit()
    session.close()
    print(f"✅ Created {len(admins)} admin users")


def seed_customers():
    """Create sample customer accounts."""
    print("Seeding customers...")
    session = get_session()
    
    # ✅ FIX: Create users directly in database instead of using AuthenticationManager
    customers = [
        {
            'email': 'john.doe@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '+1234567890',
            'city': 'New York',
            'country': 'USA'
        },
        {
            'email': 'jane.smith@example.com',
            'password': 'password123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone_number': '+1234567891',
            'city': 'Los Angeles',
            'country': 'USA'
        },
        {
            'email': 'bob.wilson@example.com',
            'password': 'password123',
            'first_name': 'Bob',
            'last_name': 'Wilson',
            'phone_number': '+1234567892',
            'city': 'Chicago',
            'country': 'USA'
        }
    ]
    
    for customer_data in customers:
        user = User(
            email=customer_data['email'],
            password_hash=AuthenticationManager.hash_password(customer_data['password']),
            first_name=customer_data['first_name'],
            last_name=customer_data['last_name'],
            phone_number=customer_data['phone_number'],
            city=customer_data.get('city'),
            country=customer_data.get('country'),
            loyalty_points=0,
            account_status='active'
        )
        session.add(user)
    
    session.commit()
    session.close()
    print(f"✅ Created {len(customers)} customers")


def seed_promo_codes():
    """Create promotional codes."""
    print("Seeding promo codes...")
    session = get_session()
    
    now = datetime.now()
    promos = [
        {
            'code': 'WELCOME10',
            'discount_percentage': 10.0,
            'valid_from': now,
            'valid_until': now + timedelta(days=365),
            'usage_limit': 100,
            'active': True
        },
        {
            'code': 'SUMMER2025',
            'discount_percentage': 15.0,
            'valid_from': datetime(2025, 6, 1),
            'valid_until': datetime(2025, 8, 31),
            'usage_limit': 200,
            'active': True
        }
    ]
    
    for promo_data in promos:
        promo = PromoCode(**promo_data)
        session.add(promo)
    
    session.commit()
    session.close()
    print(f"✅ Created {len(promos)} promo codes")


def main():
    """Run all seed functions."""
    print("=" * 60)
    print("🌱 Starting Database Seeding...")
    print("=" * 60)
    
    init_database()
    seed_rooms()
    seed_admin_users()
    seed_customers()
    seed_promo_codes()
    
    print("\n" + "=" * 60)
    print("✅ Database seeding completed!")
    print("=" * 60)
    print("\n📝 Default Credentials:")
    print("Admin - Username: admin | Password: admin123")
    print("Customer - Email: Mo.Fathi@example.com | Password: password123")
    print("=" * 60)


if __name__ == "__main__":
    main()

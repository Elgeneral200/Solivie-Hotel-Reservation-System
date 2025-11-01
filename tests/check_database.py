"""
Quick database verification script.
"""

from database.db_manager import get_db_session, DatabaseManager
from database.models import User, Room, AdminUser

print("🔍 Checking Database Contents...")
print("=" * 60)

stats = DatabaseManager.get_database_stats()

print(f"Users: {stats.get('users', 0)}")
print(f"Rooms: {stats.get('rooms', 0)}")
print(f"Admins: {stats.get('admins', 0)}")
print(f"Bookings: {stats.get('bookings', 0)}")

print("\n📋 Sample Users:")
with get_db_session() as session:
    users = session.query(User).limit(3).all()
    for user in users:
        print(f"  - {user.email}")

print("\n📋 Sample Rooms:")
with get_db_session() as session:
    rooms = session.query(Room).limit(5).all()
    for room in rooms:
        print(f"  - Room {room.room_number}: {room.room_type} - ${room.base_price_per_night}/night")

print("\n📋 Sample Admins:")
with get_db_session() as session:
    admins = session.query(AdminUser).all()
    for admin in admins:
        print(f"  - {admin.username} ({admin.role})")

print("\n" + "=" * 60)

if stats.get('users', 0) == 0:
    print("❌ Database is empty!")
    print("Run: python -m database.seed_data")
else:
    print("✅ Database has data!")

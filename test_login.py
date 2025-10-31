"""
Quick test to verify login works.
Run: python test_login.py
"""

print("Testing Login Fix...")

from backend.auth.authentication import AuthenticationManager
from backend.user.user_manager import UserManager

# Test user login
print("\n1️⃣ Testing User Login...")
success, user_id, message = AuthenticationManager.login_user(
    "john.doe@example.com",
    "password123"
)

print(f"Login: {'✅ SUCCESS' if success else '❌ FAILED'}")
print(f"Message: {message}")

if success:
    print(f"User ID: {user_id}")
    
    # Test getting user profile
    print("\n2️⃣ Testing User Profile Retrieval...")
    user = UserManager.get_user_profile(user_id)
    
    if user:
        print(f"✅ Profile Retrieved")
        # ✅ FIX: Use dictionary key access, not attribute access
        print(f"Name: {user['first_name']} {user['last_name']}")
        print(f"Email: {user['email']}")
        print(f"Phone: {user['phone_number']}")
        print(f"City: {user['city']}")
        print(f"Loyalty Points: {user['loyalty_points']}")
        print(f"Account Status: {user['account_status']}")
    else:
        print("❌ Profile Not Found")
    
    # Test statistics
    print("\n3️⃣ Testing User Statistics...")
    stats = UserManager.get_user_statistics(user_id)
    print(f"✅ Statistics Retrieved")
    print(f"Total Bookings: {stats['total_bookings']}")
    print(f"Completed Bookings: {stats['completed_bookings']}")
    print(f"Total Spent: ${stats['total_spent']:.2f}")
    print(f"Loyalty Points: {stats['loyalty_points']}")

print("\n" + "="*60)
print("✅ Login Test Complete!")
print("="*60)

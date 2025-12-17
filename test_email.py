"""
Quick email test script - Send test email to your Gmail
"""
from backend.notification.email_service import EmailService
from datetime import datetime

print("\n" + "🧪" * 35)
print("EMAIL SYSTEM TEST")
print("🧪" * 35)

# Test booking data
test_booking = {
    'guest_name': 'Muhammad Fathi (TEST)',
    'booking_reference': 'TEST-' + datetime.now().strftime('%H%M%S'),
    'room_type': 'Deluxe Suite',
    'room_number': '101',
    'check_in': 'December 20, 2025',
    'check_out': 'December 22, 2025',
    'num_guests': 2,
    'total_amount': 400.00,
    'nights': 2
}

print(f"\n📧 Sending test email to: mudiifathii@gmail.com")
print(f"📋 Booking Reference: {test_booking['booking_reference']}")
print("-" * 70)

# Send test email
result = EmailService.send_booking_confirmation(
    to_email='mudiifathii@gmail.com',
    booking_data=test_booking
)

print("-" * 70)

if result:
    print("\n✅ SUCCESS! TEST EMAIL SENT!")
    print("\n📬 NOW CHECK YOUR GMAIL:")
    print("   1. Go to: https://mail.google.com")
    print("   2. Check INBOX")
    print("   3. Also check SPAM/JUNK folder")
    print("   4. Look for: Solivie Hotel")
    print(f"   5. Subject: ✅ Booking Confirmed - {test_booking['booking_reference']}")
else:
    print("\n❌ TEST FAILED!")
    print("   Check the error messages above")

print("\n" + "🧪" * 35 + "\n")

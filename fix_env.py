"""
Create .env in TESTING MODE - Skip Gmail for now
"""

def create_testing_env():
    """Create .env file for testing mode."""
    
    env_content = """# ============================================================================
# SECURITY
# ============================================================================
SECRET_KEY=solivie-hotel-secret-key-2025

# ============================================================================
# EMAIL CONFIGURATION - TESTING MODE
# ============================================================================
EMAIL_ENABLED=False

# SMTP Server Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

# Email Credentials (empty for testing mode)
EMAIL_USER=
EMAIL_PASSWORD=

# Sender Information
EMAIL_FROM_NAME=Solivie Hotel
EMAIL_FROM=noreply@solivie.com
EMAIL_REPLY_TO=support@solivie.com

# ============================================================================
# ADMIN
# ============================================================================
ADMIN_EMAIL=admin@solivie.com
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("=" * 60)
        print("✅ TESTING MODE ENABLED")
        print("=" * 60)
        print("\n📋 Configuration:")
        print("  • EMAIL_ENABLED = False")
        print("  • Emails will print to console")
        print("  • Everything else works normally")
        print("\n🎯 What this means:")
        print("  ✅ System works completely")
        print("  ✅ Bookings succeed")
        print("  ✅ You can see email content in terminal")
        print("  ❌ Emails don't actually send (yet)")
        print("\n💡 You can enable real Gmail later from a computer!")
        print("=" * 60)
        print("\n✅ .env file created!")
        print("🚀 Ready to continue to Step 2!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    create_testing_env()

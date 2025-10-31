"""
User authentication logic.
Handles registration, login, password hashing, and verification.
"""

import bcrypt
from database.db_manager import get_db_session
from database.models import User, AdminUser
from utils.validators import validate_email, validate_password


class AuthenticationManager:
    """Manages authentication operations."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password with bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def register_user(email, password, first_name, last_name, phone_number):
        """Register new customer account."""
        if not validate_email(email):
            return False, "Invalid email format"
        
        if not validate_password(password):
            return False, "Password must be at least 8 characters with uppercase, lowercase, and numbers"
        
        try:
            with get_db_session() as session:
                existing = session.query(User).filter_by(email=email).first()
                if existing:
                    return False, "Email already registered"
                
                new_user = User(
                    email=email,
                    password_hash=AuthenticationManager.hash_password(password),
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number
                )
                session.add(new_user)
                session.commit()
                
                return True, "Registration successful"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    @staticmethod
    def login_user(email, password):
        """Authenticate customer login."""
        try:
            with get_db_session() as session:
                user = session.query(User).filter_by(email=email).first()
                
                if not user:
                    return False, None, "User not found"
                
                if user.account_status != 'active':
                    return False, None, "Account is suspended"
                
                if AuthenticationManager.verify_password(password, user.password_hash):
                    return True, user.user_id, "Login successful"
                else:
                    return False, None, "Incorrect password"
        except Exception as e:
            return False, None, f"Login failed: {str(e)}"
    
    @staticmethod
    def login_admin(username, password):
        """Authenticate admin login."""
        try:
            with get_db_session() as session:
                admin = session.query(AdminUser).filter_by(username=username).first()
                
                if not admin:
                    return False, None, None, "Admin not found"
                
                if AuthenticationManager.verify_password(password, admin.password_hash):
                    from datetime import datetime
                    admin.last_login = datetime.utcnow()
                    session.commit()
                    return True, admin.admin_id, admin.role, "Login successful"
                else:
                    return False, None, None, "Incorrect password"
        except Exception as e:
            return False, None, None, f"Login failed: {str(e)}"

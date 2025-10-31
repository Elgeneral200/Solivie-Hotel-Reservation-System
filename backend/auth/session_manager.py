"""
Session management utilities.
Handles session creation, validation, and cleanup.
"""

from datetime import datetime, timedelta
import config


class SessionManager:
    """Manages user sessions."""
    
    @staticmethod
    def create_session(user_id, user_type='customer'):
        """Create new session data."""
        return {
            'user_id': user_id,
            'user_type': user_type,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(seconds=config.SESSION_TIMEOUT)
        }
    
    @staticmethod
    def is_session_valid(session_data):
        """Check if session is still valid."""
        if not session_data:
            return False
        
        expires_at = session_data.get('expires_at')
        if not expires_at:
            return False
        
        return datetime.utcnow() < expires_at
    
    @staticmethod
    def refresh_session(session_data):
        """Refresh session expiry."""
        if session_data:
            session_data['expires_at'] = datetime.utcnow() + timedelta(seconds=config.SESSION_TIMEOUT)
        return session_data

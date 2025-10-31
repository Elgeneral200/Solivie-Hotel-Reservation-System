"""
Password management utilities.
Handles password strength checking and reset functionality.
"""

import re
import config


class PasswordManager:
    """Password utilities."""
    
    @staticmethod
    def check_password_strength(password):
        """
        Check password strength and return score (0-100).
        Returns: (score, feedback)
        """
        score = 0
        feedback = []
        
        # Check length
        if len(password) >= config.MIN_PASSWORD_LENGTH:
            score += 25
        else:
            feedback.append(f"Password should be at least {config.MIN_PASSWORD_LENGTH} characters")
        
        # Check uppercase
        if re.search(r'[A-Z]', password):
            score += 25
        else:
            feedback.append("Add uppercase letters")
        
        # Check lowercase
        if re.search(r'[a-z]', password):
            score += 25
        else:
            feedback.append("Add lowercase letters")
        
        # Check numbers
        if re.search(r'\d', password):
            score += 25
        else:
            feedback.append("Add numbers")
        
        return score, feedback
    
    @staticmethod
    def generate_reset_token(email):
        """Generate password reset token."""
        import hashlib
        import time
        
        data = f"{email}{time.time()}".encode()
        return hashlib.sha256(data).hexdigest()

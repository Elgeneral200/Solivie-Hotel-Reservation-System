"""
Tests for authentication functionality.
"""

import unittest
from backend.auth.authentication import AuthenticationManager


class TestAuthentication(unittest.TestCase):
    """Test authentication functions."""
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "TestPassword123"
        hashed = AuthenticationManager.hash_password(password)
        
        self.assertNotEqual(password, hashed)
        self.assertTrue(AuthenticationManager.verify_password(password, hashed))
        self.assertFalse(AuthenticationManager.verify_password("wrong", hashed))
    
    def test_password_validation(self):
        """Test password validation."""
        from utils.validators import validate_password
        
        self.assertTrue(validate_password("ValidPass123"))
        self.assertFalse(validate_password("short"))
        self.assertFalse(validate_password("nouppercase123"))
        self.assertFalse(validate_password("NOLOWERCASE123"))
        self.assertFalse(validate_password("NoNumbers"))


if __name__ == '__main__':
    unittest.main()

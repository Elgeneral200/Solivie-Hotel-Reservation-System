"""
Tests for database operations.
"""

import unittest
from database.models import init_database
from database.db_manager import DatabaseManager


class TestDatabase(unittest.TestCase):
    """Test database functions."""
    
    def test_database_initialization(self):
        """Test database setup."""
        result = DatabaseManager.setup_database()
        self.assertTrue(result)
    
    def test_connection(self):
        """Test database connection."""
        result = DatabaseManager.check_connection()
        self.assertTrue(result)
    
    def test_table_count(self):
        """Test table count functionality."""
        from database.models import User
        count = DatabaseManager.get_table_count(User)
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)


if __name__ == '__main__':
    unittest.main()

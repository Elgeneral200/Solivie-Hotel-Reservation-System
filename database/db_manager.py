"""
Database operations manager.
Provides session management, error handling, and audit logging.
"""

from database.models import get_session, init_database, User, Room, Booking, Payment, Review, AdminUser, PromoCode, AuditLog
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text 
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@contextmanager
def get_db_session():
    """Context manager for database sessions with auto commit/rollback."""
    session = get_session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        session.close()


class DatabaseManager:
    """Centralized database operations."""
    
    @staticmethod
    def setup_database():
        """Initialize database schema."""
        try:
            init_database()
            logger.info("Database setup completed")
            return True
        except Exception as e:
            logger.error(f"Database setup failed: {str(e)}")
            return False
    
    @staticmethod
    def log_action(user_id, action_type, description, ip_address=None):
        """Log user actions for audit trail."""
        try:
            with get_db_session() as session:
                log = AuditLog(
                    user_id=user_id,
                    action_type=action_type,
                    description=description,
                    ip_address=ip_address
                )
                session.add(log)
            logger.info(f"Action logged: {action_type} by user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to log action: {str(e)}")
            return False
    
    @staticmethod
    def check_connection():
        """
        Check if database connection is working.
        Returns True if connection successful, False otherwise.
        """
        try:
            with get_db_session() as session:
                # ✅ FIX: Wrap SQL in text()
                session.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            return False
    
    @staticmethod
    def get_table_count(model_class):
        """Get the total number of records in a table."""
        try:
            with get_db_session() as session:
                count = session.query(model_class).count()
                return count
        except Exception as e:
            logger.error(f"Failed to get table count: {str(e)}")
            return 0
    
    @staticmethod
    def bulk_insert(records):
        """Insert multiple records in a single transaction."""
        try:
            with get_db_session() as session:
                session.bulk_save_objects(records)
            logger.info(f"Successfully inserted {len(records)} records")
            return True
        except Exception as e:
            logger.error(f"Bulk insert failed: {str(e)}")
            return False
    
    @staticmethod
    def clear_table(model_class):
        """
        Clear all records from a table (useful for testing).
        WARNING: Use with caution!
        """
        try:
            with get_db_session() as session:
                count = session.query(model_class).delete()
                session.commit()
            logger.info(f"Cleared {count} records from {model_class.__tablename__}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear table: {str(e)}")
            return False
    
    @staticmethod
    def get_database_stats():
        """Get statistics about the database."""
        try:
            with get_db_session() as session:
                stats = {
                    'users': session.query(User).count(),
                    'rooms': session.query(Room).count(),
                    'bookings': session.query(Booking).count(),
                    'payments': session.query(Payment).count(),
                    'reviews': session.query(Review).count(),
                    'admins': session.query(AdminUser).count(),
                    'promo_codes': session.query(PromoCode).count()
                }
                return stats
        except Exception as e:
            logger.error(f"Failed to get database stats: {str(e)}")
            return {}

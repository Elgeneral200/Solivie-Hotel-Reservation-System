"""
Custom decorators.
Utility decorators for common functionality.
"""

import functools
import time
from utils.logger import get_logger

logger = get_logger(__name__)


def timing_decorator(func):
    """Measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper


def require_login(func):
    """Decorator to require login for Streamlit pages."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import streamlit as st
        if not st.session_state.get('logged_in', False):
            st.error("Please login to access this page")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def require_admin(func):
    """Decorator to require admin privileges."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import streamlit as st
        if not st.session_state.get('is_admin', False):
            st.error("Admin access required")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def handle_errors(func):
    """Decorator to handle and log errors."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return None
    return wrapper

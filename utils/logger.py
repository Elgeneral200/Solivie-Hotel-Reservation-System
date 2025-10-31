"""
Logging configuration.
Sets up application logging.
"""

import logging
from pathlib import Path
import config

# Create logs directory
log_dir = Path(config.BASE_DIR) / 'logs'
log_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'app.log'),
        logging.StreamHandler()
    ]
)

def get_logger(name):
    """Get logger instance."""
    return logging.getLogger(name)

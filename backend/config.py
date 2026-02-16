import os
from datetime import timedelta

class Config:
    """Application configuration"""

    # SQLite Database configuration
    SQLITE_DB_PATH = os.environ.get('SQLITE_DB_PATH') or 'database/inventory.db'


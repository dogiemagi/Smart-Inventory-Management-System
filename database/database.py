"""
SQLite Database connection and utilities
"""
import sqlite3
from backend.config import Config


def get_db_connection():
    """Create and return SQLite database connection"""
    try:
        connection = sqlite3.connect(Config.SQLITE_DB_PATH, check_same_thread=False)
        connection.row_factory = sqlite3.Row  # Return rows as dictionaries
        return connection
    except Exception as e:
        print(f"Error connecting to SQLite database: {e}")
        raise


def init_db():
    """Initialize SQLite database with users schema"""
    try:
        connection = sqlite3.connect(Config.SQLITE_DB_PATH)
        cursor = connection.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'employee',
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                created_by INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE SET NULL
            )
        """)
        # Indexes for fast lookup
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_username ON users(username)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON users(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_role ON users(role)")

        # Create default admin user (password: Admin@123)
        cursor.execute("""
            INSERT OR IGNORE INTO users 
            (username, email, password_hash, role, first_name, last_name, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            'admin',
            'admin@inventory.com',
            '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5agyPY.9F7Lca',
            'admin',
            'System',
            'Administrator',
            1
        ))

        connection.commit()
        cursor.close()
        connection.close()

        print(f"SQLite database initialized successfully at {Config.SQLITE_DB_PATH}")
        return True

    except Exception as e:
        print(f"Error initializing SQLite database: {e}")
        return False


def close_db_connection(connection):
    """Close SQLite database connection"""
    if connection:
        connection.close()


def dict_from_row(row):
    """Convert SQLite row to dictionary"""
    if row is None:
        return None
    return dict(row)


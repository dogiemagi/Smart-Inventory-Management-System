"""
Smart Inventory Management System - Main Application
"""
from flask import Flask, request, send_from_directory

from backend.config import Config
from database.database import get_db_connection, init_db
import os

# Initialize Flask app
app = Flask(__name__, static_folder='frontend', static_url_path='')
app.config.from_object(Config)

# Database connection
db = None

def get_db():
    """Get database connection"""
    global db
    if db is None:
        db = get_db_connection()
    return db

if __name__ == '__main__':
    # Initialize database on first run
    print("Starting Smart Inventory Management System...")
    print("Initializing database...")
    
    # Initialize database
    init_db()
    
    print("Server starting on http://localhost:5000")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
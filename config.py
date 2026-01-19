"""
Configuration file for Flask application
All sensitive credentials must be stored in environment variables
"""

import os
from werkzeug.security import generate_password_hash

class Config:
    # Secret key for session management (MUST be set via environment variable in production)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Admin credentials (MUST be set via environment variables)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = generate_password_hash(os.environ.get('ADMIN_PASSWORD') or 'admin123')
    
    # Email configuration (OPTIONAL - for contact form notifications)
    # If not set, contact form will still work but won't send email notifications
    EMAIL_USER = os.environ.get('EMAIL_USER')   # Your Gmail address
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')  # Gmail App Password
    NOTIFICATION_EMAIL = os.environ.get('NOTIFICATION_EMAIL', EMAIL_USER)   # Where to receive notifications
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    
    # Database
    DATABASE = 'database.db'
    
    # Flask settings
    TEMPLATES_AUTO_RELOAD = True
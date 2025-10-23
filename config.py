"""
Configuration file for the Wedding Guest List application.
Easily configure users, database settings, and app behavior here.
"""

# Application Configuration
SECRET_KEY = 'your-secret-key-change-this-in-production'
DATABASE_PATH = 'data/wedding_list.db'

# User Configuration
# Add or modify users here. Format: 'username': 'password'
# In production, you should use hashed passwords!
USERS = {
    'sarah': 'password123',
    'john': 'password123',
    'emma': 'password123',
    'michael': 'password123',
    'admin': 'admin123'
}

# Application Settings
APP_TITLE = 'Wedding Guest List'
DEBUG_MODE = True
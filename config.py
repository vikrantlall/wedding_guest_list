"""
Configuration file for the Wedding Guest List application.
Easily configure users, database settings, and app behavior here.
"""
import os

# Application Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key-change-in-railway')
DATABASE_PATH = 'data/wedding_list.db'

# User Configuration
# Add or modify users here. Format: 'username': 'password'
# In production, you should use hashed passwords!
USERS = {
    'lallfamily': 'rajaranil',
    'ginarhodes': 'grace411',
    'Grace': 'Twilight4ever',
    'Vikrant': 'june282001'
}

# Application Settings
APP_TITLE = 'Wedding Guest List'
DEBUG_MODE = False
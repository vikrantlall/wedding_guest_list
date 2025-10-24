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
    'lallfamily': b'$2b$12$4gHVQB8w.1Bp0DkabAOE8.1UQckOupKjWnOTB36AI8zsYkUCEK1fC',
    'ginarhodes': b'$2b$12$YsMG2ui12nbw4vitRYRnV.azjk6O0U1udiXi2StQH9RXa5NPCCCxa',
    'Grace': b'$2b$12$blpTO8Ye/Lo5yGgyc2UdPuvcG7399QNzTd0upTHmy3I5qx2NINCGS',
    'Vikrant': b'$2b$12$9YklwQtPBhY7/ihXfnYCleMDT0L5S.GL/Vye.WgwWDlJNTlxL/9le',
}

# Application Settings
APP_TITLE = 'Wedding Guest List'
DEBUG_MODE = False
"""
Database initialization script.
Run this script to create the database and tables.
"""

from models.database import Database
import config

if __name__ == '__main__':
    db = Database(config.DATABASE_PATH)
    db.init_db()
    print(f"Database created at: {config.DATABASE_PATH}")
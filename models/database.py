"""
Database models and operations for the Wedding Guest List application.
"""

import sqlite3
import os
from contextlib import contextmanager


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def init_db(self):
        """Initialize the database with required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS guests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    count INTEGER NOT NULL,
                    side TEXT NOT NULL CHECK(side IN ('groom', 'bride')),
                    attendance TEXT NOT NULL CHECK(attendance IN ('likely', 'unlikely')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("Database initialized successfully!")

    def add_guest(self, name, count, side, attendance):
        """Add a new guest to the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO guests (name, count, side, attendance)
                VALUES (?, ?, ?, ?)
            ''', (name, count, side, attendance))
            return cursor.lastrowid

    def get_all_guests(self):
        """Get all guests from the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM guests ORDER BY name ASC')
            return [dict(row) for row in cursor.fetchall()]

    def get_guest_by_id(self, guest_id):
        """Get a specific guest by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM guests WHERE id = ?', (guest_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_guest(self, guest_id, name, count, side, attendance):
        """Update an existing guest"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE guests 
                SET name = ?, count = ?, side = ?, attendance = ?, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (name, count, side, attendance, guest_id))
            return cursor.rowcount > 0

    def delete_guest(self, guest_id):
        """Delete a guest from the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM guests WHERE id = ?', (guest_id,))
            return cursor.rowcount > 0

    def get_statistics(self):
        """Get guest statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Total guests and total count
            cursor.execute('SELECT COUNT(*) as total_entries, SUM(count) as total_count FROM guests')
            totals = dict(cursor.fetchone())

            # Likely to come
            cursor.execute('SELECT SUM(count) as likely_count FROM guests WHERE attendance = "likely"')
            likely = cursor.fetchone()
            likely_count = likely['likely_count'] if likely['likely_count'] else 0

            # Groom's side
            cursor.execute('SELECT SUM(count) as groom_count FROM guests WHERE side = "groom"')
            groom = cursor.fetchone()
            groom_count = groom['groom_count'] if groom['groom_count'] else 0

            # Bride's side
            cursor.execute('SELECT SUM(count) as bride_count FROM guests WHERE side = "bride"')
            bride = cursor.fetchone()
            bride_count = bride['bride_count'] if bride['bride_count'] else 0

            return {
                'total': totals['total_count'] if totals['total_count'] else 0,
                'likely': likely_count,
                'groom': groom_count,
                'bride': bride_count
            }
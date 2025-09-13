#!/usr/bin/env python3
"""
Database migration script for Support CRM Backend.

This script adds missing columns to existing SQLite database tables.
Run this script when you encounter schema mismatch errors after
updating the SQLAlchemy models.

Usage:
    python migrate_db.py

The script performs the following migrations:
- Adds assigned_agent_id column to tickets table (for ticket assignment)
- Adds is_active column to users table (for user account status)
"""

import sqlite3
import os

def migrate_database():
    """
    Add missing columns to existing database tables.

    This function checks for missing columns in the database schema
    and adds them if they don't exist. It's designed to be safe to run
    multiple times (idempotent).
    """
    db_path = "crm.db"

    # Check if database file exists
    if not os.path.exists(db_path):
        print("Database file not found. No migration needed.")
        return

    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # ===== MIGRATION 1: Add assigned_agent_id to tickets table =====
        print("Checking tickets table schema...")

        # Get existing columns in tickets table
        cursor.execute("PRAGMA table_info(tickets)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'assigned_agent_id' not in columns:
            print("Adding assigned_agent_id column to tickets table...")
            cursor.execute("""
                ALTER TABLE tickets
                ADD COLUMN assigned_agent_id INTEGER REFERENCES users(id)
            """)
            print("✓ Added assigned_agent_id column to tickets table")
        else:
            print("✓ assigned_agent_id column already exists")

        # ===== MIGRATION 2: Add is_active to users table =====
        print("\nChecking users table schema...")

        # Get existing columns in users table
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'is_active' not in columns:
            print("Adding is_active column to users table...")
            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN is_active TEXT DEFAULT 'True'
            """)
            print("✓ Added is_active column to users table")
        else:
            print("✓ is_active column already exists")

        # Commit changes and close connection
        conn.commit()
        conn.close()

        print("\n✅ Database migration completed successfully!")
        print("You can now restart the server.")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        # Ensure connection is closed even if error occurs
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate_database()

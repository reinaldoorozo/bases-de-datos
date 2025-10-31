#!/usr/bin/env python3
"""
FitHome Pro - Database Initialization Script
Creates and initializes the SQLite database with sample data
"""

import sqlite3
import os
from datetime import datetime, timedelta

def create_database():
    """Create and initialize the SQLite database"""
    
    # Remove existing database if it exists
    if os.path.exists('fithome_pro.db'):
        os.remove('fithome_pro.db')
        print("Existing database removed.")
    
    # Create new database
    conn = sqlite3.connect('fithome_pro.db')
    cursor = conn.cursor()
    
    print("Creating database tables...")
    
    # Read and execute SQL schema
    with open('database/fithome_pro_sqlite.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Execute the entire script
    try:
        cursor.executescript(sql_script)
    except sqlite3.Error as e:
        print(f"Error executing script: {e}")
        # Try executing line by line
        lines = sql_script.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('--'):
                try:
                    cursor.execute(line)
                except sqlite3.Error as e:
                    print(f"Error executing line: {e}")
                    print(f"Line: {line[:100]}...")
    
    conn.commit()
    print("Database created successfully!")
    
    # Verify tables were created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Created {len(tables)} tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Verify sample data
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    user_count = cursor.fetchone()[0]
    print(f"Sample users: {user_count}")
    
    cursor.execute("SELECT COUNT(*) FROM entrenamientos")
    workout_count = cursor.fetchone()[0]
    print(f"Sample workouts: {workout_count}")
    
    cursor.execute("SELECT COUNT(*) FROM logros")
    achievement_count = cursor.fetchone()[0]
    print(f"Sample achievements: {achievement_count}")
    
    conn.close()
    print("Database initialization completed!")

if __name__ == "__main__":
    create_database()

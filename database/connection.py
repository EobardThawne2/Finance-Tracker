"""
Database connection module for SQLite
"""
import sqlite3
import os
from config import Config


def get_db_connection():
    """
    Create and return a SQLite database connection
    """
    try:
        connection = sqlite3.connect(Config.DATABASE_PATH)
        connection.row_factory = sqlite3.Row  # Enable dict-like access
        # Enable foreign key support
        connection.execute("PRAGMA foreign_keys = ON")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
        return None


def dict_from_row(row):
    """Convert sqlite3.Row to dictionary"""
    if row is None:
        return None
    return dict(row)


def execute_query(query, params=None, fetch=False, fetch_one=False):
    """
    Execute a query and optionally fetch results
    
    Args:
        query: SQL query string
        params: Query parameters (tuple)
        fetch: If True, fetch all results
        fetch_one: If True, fetch one result
    
    Returns:
        Query results or last row id for INSERT
    """
    # Convert MySQL-style %s placeholders to SQLite ? placeholders
    query = query.replace('%s', '?')
    
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = connection.cursor()
    result = None
    
    try:
        cursor.execute(query, params or ())
        
        if fetch:
            rows = cursor.fetchall()
            result = [dict_from_row(row) for row in rows]
        elif fetch_one:
            result = dict_from_row(cursor.fetchone())
        else:
            connection.commit()
            result = cursor.lastrowid
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
    
    return result


def init_database():
    """
    Initialize the database with required tables
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Create Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create Expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                base_amount REAL NOT NULL,
                currency TEXT DEFAULT 'INR',
                category TEXT NOT NULL,
                date DATE NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_expenses ON expenses(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_expense_date ON expenses(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_expense_category ON expenses(category)")
        
        connection.commit()
        print("Database initialized successfully!")
        
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

-- Finance Tracker Database Setup (SQLite)
-- The database is auto-created by the application
-- This script can be run manually with: sqlite3 finance_tracker.db < db_setup.sql

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Expenses Table
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
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_expenses ON expenses(user_id);
CREATE INDEX IF NOT EXISTS idx_expense_date ON expenses(date);
CREATE INDEX IF NOT EXISTS idx_expense_category ON expenses(category);

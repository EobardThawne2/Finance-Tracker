"""
Expense management module
"""
from database.connection import execute_query
from datetime import datetime


# Expense categories
EXPENSE_CATEGORIES = [
    'Food & Dining',
    'Transportation',
    'Shopping',
    'Entertainment',
    'Bills & Utilities',
    'Healthcare',
    'Education',
    'Travel',
    'Personal Care',
    'Groceries',
    'Rent',
    'Insurance',
    'Investments',
    'Other'
]


def add_expense(user_id, amount, category, date, description='', currency='INR', base_amount=None):
    """
    Add a new expense record
    
    Args:
        user_id: ID of the user
        amount: Original expense amount
        category: Expense category
        date: Date of expense
        description: Optional description
        currency: Currency of the expense
        base_amount: Converted amount in base currency (INR)
    
    Returns:
        expense_id if successful, None otherwise
    """
    if base_amount is None:
        base_amount = amount
    
    expense_id = execute_query(
        """INSERT INTO expenses (user_id, amount, base_amount, currency, category, date, description)
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (user_id, amount, base_amount, currency, category, date, description)
    )
    
    return expense_id


def get_expense(expense_id, user_id):
    """
    Get a single expense by ID
    
    Args:
        expense_id: ID of the expense
        user_id: ID of the user (for security)
    
    Returns:
        Expense dict or None
    """
    return execute_query(
        """SELECT * FROM expenses 
           WHERE expense_id = %s AND user_id = %s""",
        (expense_id, user_id),
        fetch_one=True
    )


def get_user_expenses(user_id, start_date=None, end_date=None, category=None, limit=None):
    """
    Get all expenses for a user with optional filters
    
    Args:
        user_id: ID of the user
        start_date: Filter by start date
        end_date: Filter by end date
        category: Filter by category
        limit: Maximum number of records
    
    Returns:
        List of expense dicts
    """
    query = "SELECT * FROM expenses WHERE user_id = %s"
    params = [user_id]
    
    if start_date:
        query += " AND date >= %s"
        params.append(start_date)
    
    if end_date:
        query += " AND date <= %s"
        params.append(end_date)
    
    if category:
        query += " AND category = %s"
        params.append(category)
    
    query += " ORDER BY date DESC"
    
    if limit:
        query += f" LIMIT {int(limit)}"
    
    return execute_query(query, tuple(params), fetch=True) or []


def update_expense(expense_id, user_id, amount=None, category=None, date=None, 
                   description=None, currency=None, base_amount=None):
    """
    Update an existing expense
    
    Args:
        expense_id: ID of the expense to update
        user_id: ID of the user (for security)
        Other args: Fields to update
    
    Returns:
        True if successful, False otherwise
    """
    updates = []
    params = []
    
    if amount is not None:
        updates.append("amount = %s")
        params.append(amount)
    
    if base_amount is not None:
        updates.append("base_amount = %s")
        params.append(base_amount)
    
    if currency is not None:
        updates.append("currency = %s")
        params.append(currency)
    
    if category is not None:
        updates.append("category = %s")
        params.append(category)
    
    if date is not None:
        updates.append("date = %s")
        params.append(date)
    
    if description is not None:
        updates.append("description = %s")
        params.append(description)
    
    if not updates:
        return False
    
    params.extend([expense_id, user_id])
    
    query = f"""UPDATE expenses SET {', '.join(updates)} 
                WHERE expense_id = %s AND user_id = %s"""
    
    result = execute_query(query, tuple(params))
    return result is not None


def delete_expense(expense_id, user_id):
    """
    Delete an expense
    
    Args:
        expense_id: ID of the expense to delete
        user_id: ID of the user (for security)
    
    Returns:
        True if successful, False otherwise
    """
    result = execute_query(
        "DELETE FROM expenses WHERE expense_id = %s AND user_id = %s",
        (expense_id, user_id)
    )
    return result is not None


def get_categories():
    """Return list of available expense categories"""
    return EXPENSE_CATEGORIES

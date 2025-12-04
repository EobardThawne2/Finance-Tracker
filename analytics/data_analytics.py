"""
Data Analytics module using Pandas
"""
import pandas as pd
from datetime import datetime, timedelta
from expenses.expense_manager import get_user_expenses
from currency.converter import convert_currency


def get_expense_dataframe(user_id, start_date=None, end_date=None):
    """
    Convert user expenses to a Pandas DataFrame
    
    Args:
        user_id: User's ID
        start_date: Optional start date filter
        end_date: Optional end date filter
    
    Returns:
        Pandas DataFrame of expenses
    """
    expenses = get_user_expenses(user_id, start_date, end_date)
    
    if not expenses:
        return pd.DataFrame()
    
    df = pd.DataFrame(expenses)
    
    # Clean and normalize data
    df = clean_expense_data(df)
    
    return df


def clean_expense_data(df):
    """
    Clean and normalize expense data
    
    Args:
        df: Raw expense DataFrame
    
    Returns:
        Cleaned DataFrame
    """
    if df.empty:
        return df
    
    # Ensure date column is datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Fill missing categories
    if 'category' in df.columns:
        df['category'] = df['category'].fillna('Other')
    
    # Fill missing descriptions
    if 'description' in df.columns:
        df['description'] = df['description'].fillna('')
    
    # Ensure numeric columns are proper type
    if 'amount' in df.columns:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    
    if 'base_amount' in df.columns:
        df['base_amount'] = pd.to_numeric(df['base_amount'], errors='coerce').fillna(0)
    
    return df


def get_monthly_summary(user_id, year=None, month=None):
    """
    Get monthly spending summary
    
    Args:
        user_id: User's ID
        year: Year (default: current)
        month: Month (default: current)
    
    Returns:
        Dict with monthly statistics
    """
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    
    df = get_expense_dataframe(user_id, start_date, end_date)
    
    if df.empty:
        return {
            'total': 0,
            'count': 0,
            'average': 0,
            'categories': {},
            'daily_avg': 0
        }
    
    total = df['base_amount'].sum()
    count = len(df)
    average = df['base_amount'].mean()
    
    # Category breakdown
    categories = df.groupby('category')['base_amount'].sum().to_dict()
    
    # Daily average
    days_in_month = (end_date - start_date).days + 1
    daily_avg = total / days_in_month
    
    return {
        'total': round(total, 2),
        'count': count,
        'average': round(average, 2),
        'categories': {k: round(v, 2) for k, v in categories.items()},
        'daily_avg': round(daily_avg, 2)
    }


def get_category_distribution(user_id, months=3):
    """
    Get category-wise spending distribution
    
    Args:
        user_id: User's ID
        months: Number of months to analyze
    
    Returns:
        Dict with category percentages
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    df = get_expense_dataframe(user_id, start_date, end_date)
    
    if df.empty:
        return {}
    
    total = df['base_amount'].sum()
    category_totals = df.groupby('category')['base_amount'].sum()
    
    return {
        cat: round((amount / total) * 100, 1) 
        for cat, amount in category_totals.items()
    }


def get_daily_spending_trend(user_id, days=30):
    """
    Get daily spending trend
    
    Args:
        user_id: User's ID
        days: Number of days to analyze
    
    Returns:
        Dict with date-wise spending
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    df = get_expense_dataframe(user_id, start_date, end_date)
    
    if df.empty:
        return {}
    
    daily = df.groupby(df['date'].dt.date)['base_amount'].sum()
    
    return {str(date): round(amount, 2) for date, amount in daily.items()}


def get_monthly_totals(user_id, months=6):
    """
    Get monthly spending totals
    
    Args:
        user_id: User's ID
        months: Number of months
    
    Returns:
        Dict with month-wise totals
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    df = get_expense_dataframe(user_id, start_date, end_date)
    
    if df.empty:
        return {}
    
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month')['base_amount'].sum()
    
    return {str(month): round(amount, 2) for month, amount in monthly.items()}


def get_spending_statistics(user_id):
    """
    Get comprehensive spending statistics
    
    Args:
        user_id: User's ID
    
    Returns:
        Dict with various statistics
    """
    # Last 30 days
    end_date = datetime.now()
    start_date_30 = end_date - timedelta(days=30)
    start_date_90 = end_date - timedelta(days=90)
    
    df_30 = get_expense_dataframe(user_id, start_date_30, end_date)
    df_90 = get_expense_dataframe(user_id, start_date_90, end_date)
    
    stats = {
        'total_30_days': 0,
        'total_90_days': 0,
        'expense_count_30_days': 0,
        'highest_category': 'N/A',
        'lowest_category': 'N/A',
        'average_expense': 0,
        'highest_expense': 0,
        'lowest_expense': 0
    }
    
    if not df_30.empty:
        stats['total_30_days'] = round(df_30['base_amount'].sum(), 2)
        stats['expense_count_30_days'] = len(df_30)
        stats['average_expense'] = round(df_30['base_amount'].mean(), 2)
        stats['highest_expense'] = round(df_30['base_amount'].max(), 2)
        stats['lowest_expense'] = round(df_30['base_amount'].min(), 2)
        
        # Category analysis
        category_totals = df_30.groupby('category')['base_amount'].sum()
        if not category_totals.empty:
            stats['highest_category'] = category_totals.idxmax()
            stats['lowest_category'] = category_totals.idxmin()
    
    if not df_90.empty:
        stats['total_90_days'] = round(df_90['base_amount'].sum(), 2)
    
    return stats


def estimate_monthly_savings(user_id, monthly_income=50000):
    """
    Estimate monthly savings based on spending patterns
    
    Args:
        user_id: User's ID
        monthly_income: Assumed monthly income
    
    Returns:
        Dict with savings estimation
    """
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_summary = get_monthly_summary(user_id, current_year, current_month)
    
    spent = monthly_summary['total']
    savings = monthly_income - spent
    savings_rate = (savings / monthly_income) * 100 if monthly_income > 0 else 0
    
    return {
        'income': monthly_income,
        'spent': round(spent, 2),
        'savings': round(savings, 2),
        'savings_rate': round(savings_rate, 1)
    }

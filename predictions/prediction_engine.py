"""
Prediction Engine using scikit-learn
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from analytics.data_analytics import get_expense_dataframe, get_monthly_totals


def prepare_training_data(user_id, months=6):
    """
    Prepare training data for the prediction model
    
    Args:
        user_id: User's ID
        months: Number of months of data to use
    
    Returns:
        Tuple of (X, y) arrays for training
    """
    monthly_data = get_monthly_totals(user_id, months)
    
    if len(monthly_data) < 2:
        return None, None
    
    # Convert to arrays
    months_list = sorted(monthly_data.keys())
    amounts = [monthly_data[m] for m in months_list]
    
    # Create feature array (month indices)
    X = np.array(range(len(amounts))).reshape(-1, 1)
    y = np.array(amounts)
    
    return X, y


def predict_next_month_spending(user_id):
    """
    Predict next month's total spending using Linear Regression
    
    Args:
        user_id: User's ID
    
    Returns:
        Dict with prediction details
    """
    X, y = prepare_training_data(user_id, months=6)
    
    if X is None or len(X) < 2:
        return {
            'prediction': None,
            'confidence': 'low',
            'message': 'Insufficient data for prediction. Need at least 2 months of data.',
            'historical_average': 0
        }
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next month
    next_month_idx = len(X)
    prediction = model.predict([[next_month_idx]])[0]
    
    # Calculate R-squared for confidence
    r_squared = model.score(X, y)
    
    # Determine confidence level
    if r_squared >= 0.7:
        confidence = 'high'
    elif r_squared >= 0.4:
        confidence = 'medium'
    else:
        confidence = 'low'
    
    # Calculate historical average
    historical_avg = np.mean(y)
    
    return {
        'prediction': round(max(0, prediction), 2),
        'confidence': confidence,
        'r_squared': round(r_squared, 3),
        'historical_average': round(historical_avg, 2),
        'trend': 'increasing' if model.coef_[0] > 0 else 'decreasing',
        'monthly_change': round(model.coef_[0], 2)
    }


def predict_category_spending(user_id, category):
    """
    Predict spending for a specific category
    
    Args:
        user_id: User's ID
        category: Expense category
    
    Returns:
        Dict with category prediction
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # 6 months
    
    df = get_expense_dataframe(user_id, start_date, end_date)
    
    if df.empty:
        return {'prediction': None, 'message': 'No data available'}
    
    # Filter by category
    df_cat = df[df['category'] == category]
    
    if df_cat.empty:
        return {'prediction': None, 'message': f'No data for category: {category}'}
    
    # Group by month
    df_cat['month'] = df_cat['date'].dt.to_period('M')
    monthly = df_cat.groupby('month')['base_amount'].sum().sort_index()
    
    if len(monthly) < 2:
        return {
            'prediction': round(monthly.mean(), 2),
            'confidence': 'low',
            'message': 'Limited data, using average'
        }
    
    # Train model
    X = np.array(range(len(monthly))).reshape(-1, 1)
    y = monthly.values
    
    model = LinearRegression()
    model.fit(X, y)
    
    prediction = model.predict([[len(X)]])[0]
    
    return {
        'prediction': round(max(0, prediction), 2),
        'historical_average': round(np.mean(y), 2),
        'confidence': 'medium' if model.score(X, y) >= 0.4 else 'low'
    }


def get_spending_forecast(user_id, months_ahead=3):
    """
    Get spending forecast for multiple months
    
    Args:
        user_id: User's ID
        months_ahead: Number of months to forecast
    
    Returns:
        List of monthly predictions
    """
    X, y = prepare_training_data(user_id, months=6)
    
    if X is None or len(X) < 2:
        return []
    
    model = LinearRegression()
    model.fit(X, y)
    
    forecasts = []
    for i in range(months_ahead):
        future_idx = len(X) + i
        prediction = model.predict([[future_idx]])[0]
        
        # Calculate month name
        future_date = datetime.now() + timedelta(days=30 * (i + 1))
        month_name = future_date.strftime('%B %Y')
        
        forecasts.append({
            'month': month_name,
            'predicted_spending': round(max(0, prediction), 2)
        })
    
    return forecasts


def analyze_spending_pattern(user_id):
    """
    Analyze user's spending pattern
    
    Args:
        user_id: User's ID
    
    Returns:
        Dict with pattern analysis
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    df = get_expense_dataframe(user_id, start_date, end_date)
    
    if df.empty:
        return {
            'pattern': 'unknown',
            'insights': ['Not enough data to analyze patterns']
        }
    
    insights = []
    
    # Analyze day of week pattern
    df['day_of_week'] = df['date'].dt.day_name()
    dow_spending = df.groupby('day_of_week')['base_amount'].sum()
    
    if not dow_spending.empty:
        peak_day = dow_spending.idxmax()
        insights.append(f"You spend most on {peak_day}s")
    
    # Analyze category pattern
    category_spending = df.groupby('category')['base_amount'].sum().sort_values(ascending=False)
    if not category_spending.empty:
        top_category = category_spending.index[0]
        top_percentage = (category_spending.iloc[0] / category_spending.sum()) * 100
        insights.append(f"{top_category} accounts for {round(top_percentage, 1)}% of your spending")
    
    # Analyze trend
    prediction_data = predict_next_month_spending(user_id)
    if prediction_data['prediction']:
        if prediction_data['trend'] == 'increasing':
            insights.append(f"Your spending is trending upward by ₹{abs(prediction_data['monthly_change'])}/month")
        else:
            insights.append(f"Your spending is trending downward by ₹{abs(prediction_data['monthly_change'])}/month")
    
    return {
        'pattern': prediction_data.get('trend', 'stable'),
        'insights': insights,
        'top_categories': dict(category_spending.head(3)),
        'peak_spending_day': peak_day if not dow_spending.empty else 'Unknown'
    }

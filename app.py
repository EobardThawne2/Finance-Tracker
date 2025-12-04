"""
Flask Application - Finance Tracker with Predictions
Main application file with all routes
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from database.connection import init_database
from auth.auth_module import create_user, authenticate_user, get_user_by_id
from expenses.expense_manager import (
    add_expense, get_expense, get_user_expenses, 
    update_expense, delete_expense, get_categories
)
from currency.converter import (
    convert_currency, get_supported_currencies, 
    get_exchange_rate, fetch_exchange_rates
)
from analytics.data_analytics import (
    get_monthly_summary, get_category_distribution,
    get_daily_spending_trend, get_spending_statistics,
    estimate_monthly_savings, get_monthly_totals
)
from predictions.prediction_engine import (
    predict_next_month_spending, get_spending_forecast,
    analyze_spending_pattern
)
from visualizations.charts import (
    create_monthly_spending_chart, create_category_bar_chart,
    create_daily_trend_chart, create_prediction_comparison_chart,
    create_pie_chart
)

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== Public Routes ====================

@app.route('/')
def index():
    """Landing page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Please provide username and password.', 'error')
            return render_template('login.html')
        
        user = authenticate_user(username, password)
        
        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['email'] = user['email']
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=7)
            
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('register.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        # Create user
        user_id = create_user(username, email, password)
        
        if user_id:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists.', 'error')
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ==================== Protected Routes ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with summary and charts"""
    user_id = session['user_id']
    
    # Get summary data
    current_month = datetime.now()
    monthly_summary = get_monthly_summary(user_id, current_month.year, current_month.month)
    
    # Get prediction
    prediction = predict_next_month_spending(user_id)
    
    # Get recent expenses
    recent_expenses = get_user_expenses(user_id, limit=5)
    
    # Get statistics
    stats = get_spending_statistics(user_id)
    
    # Generate charts
    monthly_chart = create_monthly_spending_chart(user_id)
    category_chart = create_pie_chart(user_id)
    
    return render_template('dashboard.html',
        monthly_summary=monthly_summary,
        prediction=prediction,
        recent_expenses=recent_expenses,
        stats=stats,
        monthly_chart=monthly_chart,
        category_chart=category_chart
    )


@app.route('/add-expense', methods=['GET', 'POST'])
@login_required
def add_expense_page():
    """Add new expense page"""
    user_id = session['user_id']
    categories = get_categories()
    currencies = get_supported_currencies()
    
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            category = request.form.get('category', '')
            date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
            description = request.form.get('description', '')
            currency = request.form.get('currency', 'INR')
            
            if amount <= 0:
                flash('Amount must be greater than 0.', 'error')
                return render_template('add_expense.html', 
                    categories=categories, currencies=currencies)
            
            if not category:
                flash('Please select a category.', 'error')
                return render_template('add_expense.html', 
                    categories=categories, currencies=currencies)
            
            # Convert to base currency (INR)
            base_amount = convert_currency(amount, currency, 'INR')
            
            expense_id = add_expense(
                user_id=user_id,
                amount=amount,
                category=category,
                date=date,
                description=description,
                currency=currency,
                base_amount=base_amount
            )
            
            if expense_id:
                flash('Expense added successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Failed to add expense. Please try again.', 'error')
                
        except ValueError:
            flash('Invalid amount entered.', 'error')
    
    return render_template('add_expense.html', 
        categories=categories, 
        currencies=currencies,
        today=datetime.now().strftime('%Y-%m-%d'))


@app.route('/edit-expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense_page(expense_id):
    """Edit expense page"""
    user_id = session['user_id']
    expense = get_expense(expense_id, user_id)
    
    if not expense:
        flash('Expense not found.', 'error')
        return redirect(url_for('dashboard'))
    
    categories = get_categories()
    currencies = get_supported_currencies()
    
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            category = request.form.get('category', '')
            date = request.form.get('date', '')
            description = request.form.get('description', '')
            currency = request.form.get('currency', 'INR')
            
            if amount <= 0:
                flash('Amount must be greater than 0.', 'error')
                return render_template('edit_expense.html', 
                    expense=expense, categories=categories, currencies=currencies)
            
            # Convert to base currency (INR)
            base_amount = convert_currency(amount, currency, 'INR')
            
            success = update_expense(
                expense_id=expense_id,
                user_id=user_id,
                amount=amount,
                category=category,
                date=date,
                description=description,
                currency=currency,
                base_amount=base_amount
            )
            
            if success:
                flash('Expense updated successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Failed to update expense.', 'error')
                
        except ValueError:
            flash('Invalid amount entered.', 'error')
    
    return render_template('edit_expense.html', 
        expense=expense, 
        categories=categories, 
        currencies=currencies)


@app.route('/delete-expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense_route(expense_id):
    """Delete expense"""
    user_id = session['user_id']
    
    success = delete_expense(expense_id, user_id)
    
    if success:
        flash('Expense deleted successfully!', 'success')
    else:
        flash('Failed to delete expense.', 'error')
    
    return redirect(url_for('dashboard'))


@app.route('/expenses')
@login_required
def expenses_list():
    """List all expenses with filters"""
    user_id = session['user_id']
    
    # Get filter parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')
    
    expenses = get_user_expenses(user_id, start_date, end_date, category)
    categories = get_categories()
    
    return render_template('expenses.html', 
        expenses=expenses, 
        categories=categories,
        filters={
            'start_date': start_date,
            'end_date': end_date,
            'category': category
        })


@app.route('/analytics')
@login_required
def analytics_page():
    """Full analytics page with Pandas data"""
    user_id = session['user_id']
    
    # Get all analytics data
    current_month = datetime.now()
    monthly_summary = get_monthly_summary(user_id, current_month.year, current_month.month)
    category_distribution = get_category_distribution(user_id)
    daily_trend = get_daily_spending_trend(user_id, 30)
    monthly_totals = get_monthly_totals(user_id, 6)
    stats = get_spending_statistics(user_id)
    savings = estimate_monthly_savings(user_id)
    
    # Generate charts
    monthly_chart = create_monthly_spending_chart(user_id)
    category_bar_chart = create_category_bar_chart(user_id)
    daily_trend_chart = create_daily_trend_chart(user_id)
    pie_chart = create_pie_chart(user_id)
    
    return render_template('analytics.html',
        monthly_summary=monthly_summary,
        category_distribution=category_distribution,
        daily_trend=daily_trend,
        monthly_totals=monthly_totals,
        stats=stats,
        savings=savings,
        monthly_chart=monthly_chart,
        category_bar_chart=category_bar_chart,
        daily_trend_chart=daily_trend_chart,
        pie_chart=pie_chart
    )


@app.route('/predict')
@login_required
def predict_page():
    """ML prediction page"""
    user_id = session['user_id']
    
    # Get predictions
    next_month_prediction = predict_next_month_spending(user_id)
    forecast = get_spending_forecast(user_id, 3)
    pattern_analysis = analyze_spending_pattern(user_id)
    
    # Get comparison chart
    comparison_chart = create_prediction_comparison_chart(user_id)
    monthly_chart = create_monthly_spending_chart(user_id)
    
    return render_template('predict.html',
        prediction=next_month_prediction,
        forecast=forecast,
        pattern_analysis=pattern_analysis,
        comparison_chart=comparison_chart,
        monthly_chart=monthly_chart
    )


# ==================== API Routes ====================

@app.route('/api/rates')
def api_rates():
    """API endpoint for exchange rates"""
    base = request.args.get('base', 'USD')
    rates = fetch_exchange_rates(base)
    
    return jsonify({
        'success': True,
        'base': base,
        'rates': rates
    })


@app.route('/api/convert')
def api_convert():
    """API endpoint for currency conversion"""
    try:
        amount = float(request.args.get('amount', 0))
        from_currency = request.args.get('from', 'USD')
        to_currency = request.args.get('to', 'INR')
        
        converted = convert_currency(amount, from_currency, to_currency)
        rate = get_exchange_rate(from_currency, to_currency)
        
        return jsonify({
            'success': True,
            'original': amount,
            'from': from_currency,
            'to': to_currency,
            'converted': converted,
            'rate': rate
        })
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Invalid amount'
        }), 400


@app.route('/api/summary')
@login_required
def api_summary():
    """API endpoint for spending summary"""
    user_id = session['user_id']
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    summary = get_monthly_summary(user_id, year, month)
    
    return jsonify({
        'success': True,
        'summary': summary
    })


@app.route('/api/prediction')
@login_required
def api_prediction():
    """API endpoint for spending prediction"""
    user_id = session['user_id']
    
    prediction = predict_next_month_spending(user_id)
    
    return jsonify({
        'success': True,
        'prediction': prediction
    })


# ==================== Error Handlers ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


# ==================== Main ====================

if __name__ == '__main__':
    # Initialize database
    print("Initializing database...")
    init_database()
    
    # Run the app
    print("Starting Finance Tracker...")
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
Visualization module using Matplotlib
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64
from datetime import datetime, timedelta
import numpy as np
from analytics.data_analytics import (
    get_monthly_totals,
    get_category_distribution,
    get_daily_spending_trend,
    get_expense_dataframe
)
from predictions.prediction_engine import predict_next_month_spending


def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100, facecolor='white')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_str


def create_monthly_spending_chart(user_id, months=6):
    """
    Create monthly spending line chart
    
    Args:
        user_id: User's ID
        months: Number of months to display
    
    Returns:
        Base64 encoded PNG image
    """
    monthly_data = get_monthly_totals(user_id, months)
    
    if not monthly_data:
        return create_empty_chart("No monthly data available")
    
    months_list = sorted(monthly_data.keys())
    amounts = [monthly_data[m] for m in months_list]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.plot(months_list, amounts, marker='o', linewidth=2, markersize=8, color='#4F46E5')
    ax.fill_between(months_list, amounts, alpha=0.2, color='#4F46E5')
    
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Spending (₹)', fontsize=12)
    ax.set_title('Monthly Spending Trend', fontsize=14, fontweight='bold')
    
    # Format y-axis with commas
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
    
    plt.xticks(rotation=45)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    return fig_to_base64(fig)


def create_category_bar_chart(user_id, months=3):
    """
    Create category-wise spending bar chart
    
    Args:
        user_id: User's ID
        months: Number of months to analyze
    
    Returns:
        Base64 encoded PNG image
    """
    category_data = get_category_distribution(user_id, months)
    
    if not category_data:
        return create_empty_chart("No category data available")
    
    # Sort by value
    sorted_data = dict(sorted(category_data.items(), key=lambda x: x[1], reverse=True))
    
    categories = list(sorted_data.keys())
    percentages = list(sorted_data.values())
    
    # Color palette
    colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.barh(categories, percentages, color=colors)
    
    # Add percentage labels
    for bar, pct in zip(bars, percentages):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{pct}%', va='center', fontsize=10)
    
    ax.set_xlabel('Percentage (%)', fontsize=12)
    ax.set_title('Spending by Category', fontsize=14, fontweight='bold')
    ax.set_xlim(0, max(percentages) * 1.2)
    
    plt.tight_layout()
    
    return fig_to_base64(fig)


def create_daily_trend_chart(user_id, days=30):
    """
    Create daily spending trend plot
    
    Args:
        user_id: User's ID
        days: Number of days to display
    
    Returns:
        Base64 encoded PNG image
    """
    daily_data = get_daily_spending_trend(user_id, days)
    
    if not daily_data:
        return create_empty_chart("No daily data available")
    
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in sorted(daily_data.keys())]
    amounts = [daily_data[d.strftime('%Y-%m-%d')] for d in dates]
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    ax.bar(dates, amounts, color='#10B981', alpha=0.8)
    
    # Add trend line
    if len(dates) > 1:
        z = np.polyfit(range(len(dates)), amounts, 1)
        p = np.poly1d(z)
        ax.plot(dates, p(range(len(dates))), "r--", linewidth=2, label='Trend')
        ax.legend()
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Spending (₹)', fontsize=12)
    ax.set_title(f'Daily Spending (Last {days} Days)', fontsize=14, fontweight='bold')
    
    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days // 10)))
    
    plt.xticks(rotation=45)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
    
    return fig_to_base64(fig)


def create_prediction_comparison_chart(user_id):
    """
    Create chart comparing predictions with actual spending
    
    Args:
        user_id: User's ID
    
    Returns:
        Base64 encoded PNG image
    """
    monthly_data = get_monthly_totals(user_id, 6)
    prediction = predict_next_month_spending(user_id)
    
    if not monthly_data:
        return create_empty_chart("No data for prediction comparison")
    
    months_list = sorted(monthly_data.keys())
    actual = [monthly_data[m] for m in months_list]
    
    # Add prediction for next month
    if prediction['prediction']:
        next_month = (datetime.now() + timedelta(days=30)).strftime('%Y-%m')
        months_list.append(next_month)
        actual.append(None)  # No actual for future
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot actual spending
    ax.plot(months_list[:-1], actual[:-1], marker='o', linewidth=2, 
            markersize=8, color='#4F46E5', label='Actual')
    
    # Plot prediction
    if prediction['prediction']:
        ax.scatter([months_list[-1]], [prediction['prediction']], 
                  s=100, color='#EF4444', marker='*', zorder=5, label='Prediction')
        
        # Connect last actual to prediction with dotted line
        ax.plot([months_list[-2], months_list[-1]], 
               [actual[-2], prediction['prediction']], 
               'r--', linewidth=2)
    
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Spending (₹)', fontsize=12)
    ax.set_title('Spending: Actual vs Prediction', fontsize=14, fontweight='bold')
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
    plt.xticks(rotation=45)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    
    return fig_to_base64(fig)


def create_pie_chart(user_id, months=3):
    """
    Create pie chart for category distribution
    
    Args:
        user_id: User's ID
        months: Number of months to analyze
    
    Returns:
        Base64 encoded PNG image
    """
    category_data = get_category_distribution(user_id, months)
    
    if not category_data:
        return create_empty_chart("No category data available")
    
    labels = list(category_data.keys())
    sizes = list(category_data.values())
    
    # Colors
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(labels)))
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                       colors=colors, startangle=90,
                                       explode=[0.02] * len(labels))
    
    ax.set_title('Expense Distribution by Category', fontsize=14, fontweight='bold')
    
    # Make percentage text more readable
    for autotext in autotexts:
        autotext.set_fontsize(9)
    
    return fig_to_base64(fig)


def create_empty_chart(message):
    """
    Create a placeholder chart with a message
    
    Args:
        message: Message to display
    
    Returns:
        Base64 encoded PNG image
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.text(0.5, 0.5, message, ha='center', va='center', fontsize=14, color='gray')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    return fig_to_base64(fig)

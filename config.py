"""
Configuration settings for Finance Tracker application
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # SQLite Database settings
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or os.path.join(BASE_DIR, 'finance_tracker.db')
    
    # ExchangeRate-API settings
    EXCHANGE_API_KEY = os.environ.get('EXCHANGE_API_KEY') or 'your-api-key-here'
    EXCHANGE_API_URL = 'https://v6.exchangerate-api.com/v6/'
    
    # Default currency
    DEFAULT_CURRENCY = 'INR'
    
    # Cache settings (in seconds)
    RATE_CACHE_DURATION = 43200  # 12 hours

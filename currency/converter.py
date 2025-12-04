"""
Currency conversion module using ExchangeRate-API
"""
import requests
import time
from config import Config


# Cache for exchange rates
_rate_cache = {
    'rates': {},
    'timestamp': 0,
    'base_currency': 'USD'
}


def fetch_exchange_rates(base_currency='USD'):
    """
    Fetch latest exchange rates from API
    
    Args:
        base_currency: Base currency for rates
    
    Returns:
        Dict of exchange rates or None on error
    """
    global _rate_cache
    
    # Check cache
    current_time = time.time()
    if (_rate_cache['rates'] and 
        _rate_cache['base_currency'] == base_currency and
        current_time - _rate_cache['timestamp'] < Config.RATE_CACHE_DURATION):
        return _rate_cache['rates']
    
    try:
        url = f"{Config.EXCHANGE_API_URL}{Config.EXCHANGE_API_KEY}/latest/{base_currency}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('result') == 'success':
            _rate_cache['rates'] = data.get('conversion_rates', {})
            _rate_cache['timestamp'] = current_time
            _rate_cache['base_currency'] = base_currency
            return _rate_cache['rates']
        else:
            print(f"API Error: {data.get('error-type', 'Unknown error')}")
            return get_fallback_rates()
            
    except requests.RequestException as e:
        print(f"Request error fetching rates: {e}")
        return get_fallback_rates()


def get_fallback_rates():
    """
    Return fallback exchange rates when API is unavailable
    These are approximate rates and should only be used as backup
    """
    return {
        'USD': 1.0,
        'INR': 83.0,
        'EUR': 0.92,
        'GBP': 0.79,
        'JPY': 149.0,
        'AUD': 1.53,
        'CAD': 1.36,
        'CNY': 7.24,
        'SGD': 1.34,
        'AED': 3.67
    }


def convert_currency(amount, from_currency, to_currency='INR'):
    """
    Convert amount from one currency to another
    
    Args:
        amount: Amount to convert
        from_currency: Source currency code
        to_currency: Target currency code
    
    Returns:
        Converted amount
    """
    if from_currency == to_currency:
        return amount
    
    rates = fetch_exchange_rates('USD')
    
    if not rates:
        return amount  # Return original if conversion fails
    
    # Convert to USD first (if not already USD)
    if from_currency != 'USD':
        from_rate = rates.get(from_currency, 1)
        amount_usd = amount / from_rate
    else:
        amount_usd = amount
    
    # Convert from USD to target currency
    to_rate = rates.get(to_currency, 1)
    converted_amount = amount_usd * to_rate
    
    return round(converted_amount, 2)


def get_supported_currencies():
    """
    Get list of supported currencies
    
    Returns:
        List of currency codes with INR prioritized first
    """
    rates = fetch_exchange_rates('USD')
    if rates:
        currency_list = list(rates.keys())
        # Ensure INR is in the list and move it to the front
        if 'INR' in currency_list:
            currency_list.remove('INR')
        currency_list.insert(0, 'INR')
        return currency_list
    return ['INR', 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CNY', 'SGD', 'AED']


def get_exchange_rate(from_currency, to_currency='INR'):
    """
    Get exchange rate between two currencies
    
    Args:
        from_currency: Source currency code
        to_currency: Target currency code
    
    Returns:
        Exchange rate as float
    """
    if from_currency == to_currency:
        return 1.0
    
    rates = fetch_exchange_rates('USD')
    
    if not rates:
        return 1.0
    
    from_rate = rates.get(from_currency, 1)
    to_rate = rates.get(to_currency, 1)
    
    return round(to_rate / from_rate, 4)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.x-green?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/SQLite-3-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

<h1 align="center">💰 Finance Tracker</h1>

<p align="center">
  <strong>A comprehensive personal finance management application with spending predictions, analytics, and multi-currency support.</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-configuration">Configuration</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-project-structure">Project Structure</a> •
  <a href="#-api-reference">API Reference</a>
</p>

---

## ✨ Features

### 📊 Expense Management
- **Add, Edit, Delete Expenses** - Full CRUD operations for expense tracking
- **Categorization** - 14 predefined categories including Food, Transportation, Shopping, Bills, Healthcare, and more
- **Date-based Filtering** - View expenses by custom date ranges

### 💱 Multi-Currency Support
- **Real-time Conversion** - Integration with ExchangeRate-API for live exchange rates
- **10+ Currencies** - Support for USD, EUR, GBP, JPY, INR, AUD, CAD, CNY, SGD, AED
- **Fallback Rates** - Offline capability with cached/fallback exchange rates
- **Auto-conversion** - Automatic conversion to base currency (INR)

### 📈 Analytics & Insights
- **Monthly Summaries** - Track spending patterns month over month
- **Category Distribution** - Visualize where your money goes
- **Daily Spending Trends** - Analyze day-to-day spending habits
- **Spending Statistics** - Comprehensive stats including averages, totals, and comparisons

### 🔮 ML-Powered Predictions
- **Next Month Forecast** - Linear regression-based spending predictions
- **Confidence Levels** - R-squared based confidence indicators (High/Medium/Low)
- **Spending Pattern Analysis** - Identify trends and anomalies
- **Historical Comparisons** - Compare predictions with actual spending

### 📉 Data Visualizations
- **Line Charts** - Monthly spending trends
- **Bar Charts** - Category-wise spending breakdown
- **Pie Charts** - Proportional spending distribution
- **Prediction Charts** - Actual vs predicted spending comparisons

### 🔐 Security
- **Secure Authentication** - SHA-256 password hashing with unique salts
- **Session Management** - Flask session-based authentication with 7-day persistence
- **Protected Routes** - Login-required decorator for sensitive endpoints

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Python 3.12, Flask 3.x |
| **Database** | SQLite 3 |
| **Data Analysis** | Pandas, NumPy |
| **Machine Learning** | scikit-learn (Linear Regression) |
| **Visualization** | Matplotlib |
| **Currency API** | ExchangeRate-API |
| **Frontend** | HTML5, CSS3, JavaScript, Jinja2 |

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

> **Note:** SQLite comes bundled with Python, so no separate database installation is required!

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv ftracker
ftracker\Scripts\activate

# macOS/Linux
python3 -m venv ftracker
source ftracker/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Database

The SQLite database will be automatically created when you first run the application. The database file (`finance_tracker.db`) will be stored in the project root directory.

Alternatively, you can manually initialize the database:

```sql
-- SQLite schema (database/db_setup.sql)

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
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-super-secret-key-here
DATABASE_PATH=finance_tracker.db
EXCHANGE_API_KEY=your-exchangerate-api-key
```

### Step 6: Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | `your-secret-key-change-in-production` |
| `DATABASE_PATH` | Path to SQLite database file | `finance_tracker.db` |
| `EXCHANGE_API_KEY` | ExchangeRate-API key | `your-api-key-here` |

### Application Settings (config.py)

| Setting | Description | Default |
|---------|-------------|---------|
| `DEFAULT_CURRENCY` | Base currency for calculations | `INR` |
| `RATE_CACHE_DURATION` | Exchange rate cache duration (seconds) | `43200` (12 hours) |

---

## 🚀 Usage

### User Registration & Login

1. Navigate to `/register` to create a new account
2. Login at `/login` with your credentials
3. Sessions persist for 7 days

### Managing Expenses

1. **Add Expense**: Navigate to "Add Expense" from the dashboard
2. **View Expenses**: Browse all expenses with filtering options
3. **Edit/Delete**: Click on any expense to modify or remove

### Viewing Analytics

1. Access the Analytics page from the navigation
2. View spending breakdowns by category and time period
3. Analyze trends with interactive charts

### Getting Predictions

1. Navigate to the Predictions page
2. View ML-based spending forecasts
3. Check confidence levels and historical comparisons

---

## 📁 Project Structure

```
finance_tracker/
├── app.py                    # Main Flask application with routes
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
│
├── analytics/                # Data analytics module
│   ├── __init__.py
│   └── data_analytics.py     # Pandas-based analytics functions
│
├── auth/                     # Authentication module
│   ├── __init__.py
│   └── auth_module.py        # SHA-256 auth with salt
│
├── currency/                 # Currency conversion module
│   ├── __init__.py
│   └── converter.py          # ExchangeRate-API integration
│
├── database/                 # Database layer
│   ├── __init__.py
│   ├── connection.py         # SQLite connection handling
│   └── db_setup.sql          # Database schema
│
├── expenses/                 # Expense management module
│   ├── __init__.py
│   └── expense_manager.py    # CRUD operations for expenses
│
├── predictions/              # ML predictions module
│   ├── __init__.py
│   └── prediction_engine.py  # scikit-learn predictions
│
├── visualizations/           # Chart generation module
│   ├── __init__.py
│   └── charts.py             # Matplotlib visualizations
│
├── static/                   # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── templates/                # Jinja2 templates
│   ├── base.html             # Base template
│   ├── index.html            # Landing page
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── dashboard.html        # User dashboard
│   ├── expenses.html         # Expense list
│   ├── add_expense.html      # Add expense form
│   ├── edit_expense.html     # Edit expense form
│   ├── analytics.html        # Analytics dashboard
│   ├── predict.html          # Predictions page
│   ├── 404.html              # Not found page
│   └── 500.html              # Server error page
│
└── ftracker/                 # Virtual environment
```

---

## 📚 API Reference

### Routes

#### Public Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page |
| `/login` | GET, POST | User login |
| `/register` | GET, POST | User registration |

#### Protected Routes (Login Required)

| Route | Method | Description |
|-------|--------|-------------|
| `/dashboard` | GET | User dashboard with summary |
| `/expenses` | GET | List all expenses |
| `/add_expense` | GET, POST | Add new expense |
| `/edit_expense/<id>` | GET, POST | Edit existing expense |
| `/delete_expense/<id>` | POST | Delete expense |
| `/analytics` | GET | Analytics dashboard |
| `/predict` | GET | Spending predictions |
| `/logout` | GET | User logout |

### Expense Categories

```python
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
```

### Supported Currencies

| Code | Currency |
|------|----------|
| USD | US Dollar |
| INR | Indian Rupee |
| EUR | Euro |
| GBP | British Pound |
| JPY | Japanese Yen |
| AUD | Australian Dollar |
| CAD | Canadian Dollar |
| CNY | Chinese Yuan |
| SGD | Singapore Dollar |
| AED | UAE Dirham |

---

## 🧪 Module Documentation

### Analytics Module (`analytics/data_analytics.py`)

```python
# Get monthly spending summary
get_monthly_summary(user_id, year=None, month=None)

# Get category distribution
get_category_distribution(user_id, months=3)

# Get daily spending trend
get_daily_spending_trend(user_id, days=30)

# Get comprehensive spending statistics
get_spending_statistics(user_id)
```

### Prediction Engine (`predictions/prediction_engine.py`)

```python
# Predict next month's spending
predict_next_month_spending(user_id)
# Returns: { prediction, confidence, message, historical_average }

# Get multi-month forecast
get_spending_forecast(user_id, months=3)

# Analyze spending patterns
analyze_spending_pattern(user_id)
```

### Currency Converter (`currency/converter.py`)

```python
# Convert between currencies
convert_currency(amount, from_currency, to_currency='INR')

# Get current exchange rate
get_exchange_rate(from_currency, to_currency)

# List supported currencies
get_supported_currencies()
```

---

## 🔒 Security Considerations

1. **Password Hashing**: Uses SHA-256 with unique 16-byte salts per user
2. **Session Security**: Flask sessions with configurable secret key
3. **SQL Injection Prevention**: Parameterized queries throughout
4. **User Data Isolation**: All expense queries filtered by user_id
5. **CSRF Protection**: Form-based operations protected

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

If you have any questions or run into issues, please open an issue on GitHub.

---

<p align="center">
  Made with ❤️ by Finance Tracker Team
</p>

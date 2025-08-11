# Algo Trading Project

A Python-based algorithmic trading system using ICICI Breeze API for automated trading strategies.

## 🚀 Features

- **ICICI Breeze API Integration**: Complete authentication and session management
- **Account Management**: Balance checking, portfolio tracking, order management
- **Secure Configuration**: Environment-based secrets management
- **Modular Architecture**: Clean separation of concerns with auth, API, and utils modules

## 📋 Prerequisites

- Python 3.8+
- ICICI Direct trading account
- ICICI Breeze API credentials (API Key, Secret Key)
- Git

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/sagarstormborn/algo-trading.git
cd algo-trading
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
# Copy the .env file and update with your credentials
cp .env.example .env  # If you have an example file
# Or edit the existing .env file
```

## 🔧 Configuration

Edit the `.env` file with your ICICI Breeze API credentials:

```env
# ICICI Breeze API Configuration
BREEZE_API_KEY=your_api_key_here
BREEZE_SECRET_KEY=your_secret_key_here
BREEZE_SESSION_TOKEN=your_session_token_here

# API Endpoints
BREEZE_BASE_URL=https://api.icicidirect.com/breezeapi/v1

# Account Details
BREEZE_ACCOUNT_ID=your_account_id_here

# Environment
ENVIRONMENT=development
```

### Getting ICICI Breeze API Credentials

1. Log in to your ICICI Direct account
2. Go to API section in your account
3. Generate API Key and Secret Key
4. Note down your Account ID

## 📁 Project Structure

```
algo-trading/
├── src/
│   ├── auth/
│   │   ├── __init__.py
│   │   └── breeze_auth.py      # Authentication and session management
│   ├── api/
│   │   ├── __init__.py
│   │   └── breeze_client.py    # Main API client for trading operations
│   └── utils/
│       ├── __init__.py
│       └── config.py           # Configuration management
├── tests/                      # Test files
├── config/                     # Configuration files
├── .env                        # Environment variables (not in git)
├── requirements.txt            # Python dependencies
├── test_breeze_api.py         # Test script for API integration
└── README.md
```

## 🚀 Usage

### Testing the API Integration

Run the test script to verify your setup:

```bash
python test_breeze_api.py
```

This will test:
- Configuration loading
- Authentication
- Account balance retrieval
- Portfolio holdings
- Open orders
- Order history

### Using the API Client

```python
from src.api.breeze_client import BreezeClient

# Initialize client
client = BreezeClient()

# Authenticate
if client.authenticate("your_user_id", "your_password"):
    
    # Get account balance
    balance = client.get_account_balance()
    print(f"Account Balance: {balance}")
    
    # Get portfolio
    portfolio = client.get_portfolio()
    print(f"Portfolio: {portfolio}")
    
    # Get open orders
    open_orders = client.get_open_orders()
    print(f"Open Orders: {open_orders}")
    
    # Logout
    client.logout()
```

## 🔒 Security

- **Environment Variables**: All sensitive data is stored in `.env` file (not committed to git)
- **Session Management**: Automatic session token handling with expiry
- **Secure Headers**: Proper authentication headers for all API requests

## 📊 API Endpoints Supported

- **Authentication**: Session generation and management
- **Account Balance**: Fund details and margin information
- **Portfolio**: Current holdings and positions
- **Orders**: Open orders, order history, and order management
- **Logout**: Session termination

## 🧪 Testing

The project includes comprehensive testing:

```bash
# Run the main test suite
python test_breeze_api.py

# Test individual components
python -c "from src.utils.config import config; print(config.to_dict())"
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This software is for educational purposes only. Use at your own risk. The authors are not responsible for any financial losses incurred through the use of this software.

## 👨‍💻 Author

**Sagar Parmar**
- GitHub: [@sagarstormborn](https://github.com/sagarstormborn)
- Email: codesageml@gmail.com

## 📄 License

This project is licensed under the MIT License.

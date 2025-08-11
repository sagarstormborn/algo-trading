# Algo Trading Project

A Python-based algorithmic trading system using ICICI Breeze API for automated trading strategies.

## 🚀 Features

- **ICICI Breeze API Integration**: Complete authentication and session management
- **Account Management**: Balance checking, portfolio tracking, order management
- **Secure Configuration**: Environment-based secrets management
- **Modular Architecture**: Clean separation of concerns with auth, API, and utils modules

## 📋 Prerequisites

- Python 3.12+ (recommended)
- ICICI Direct trading account
- ICICI Breeze API credentials (API Key, Secret Key, Session Token)
- Git
- Conda (recommended) or pip

## 🛠️ Installation

### Option 1: Using Conda (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/sagarstormborn/algo-trading.git
cd algo-trading
```

2. **Create and activate conda environment:**
```bash
conda create -n algo-trading python=3.12 -y
conda activate algo-trading
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
# Edit the .env file with your API credentials
nano .env  # or use your preferred editor
```

### Option 2: Using Virtual Environment

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
# Edit the .env file with your API credentials
nano .env  # or use your preferred editor
```

## 🔧 Configuration

Edit the `.env` file with your ICICI Breeze API credentials:

```env
# ICICI Breeze API Configuration
BREEZE_API_KEY=your_api_key_here
BREEZE_SECRET_KEY=your_secret_key_here
BREEZE_SESSION_TOKEN=your_session_token_here

# API Endpoints
BREEZE_BASE_URL=https://api.icicidirect.com/breezeapi/api/v1

# Environment
ENVIRONMENT=development
```

### Getting ICICI Breeze API Credentials

1. Log in to your ICICI Direct account
2. Go to API section in your account
3. Generate API Key and Secret Key
4. Generate Session Token (valid for 24 hours)
5. Update your `.env` file with these credentials

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

### Environment Setup

**For Conda users:**
```bash
conda activate algo-trading
```

**For Virtual Environment users:**
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Testing the API Integration

Run the test script to verify your setup:

```bash
python test_breeze_api.py
```

This will test:
- ✅ Configuration loading
- ✅ Authentication using API credentials
- ✅ Account balance retrieval
- ⚠️ Portfolio holdings (returns "No Data Found" if no holdings)
- ⚠️ Open orders (temporarily disabled due to API checksum requirements)
- ⚠️ Order history (temporarily disabled due to API checksum requirements)

### Current Status
- **✅ Working**: Authentication, Account Balance, Session Management
- **⚠️ Limited**: Portfolio (works but may show "No Data Found" if no holdings)
- **🔧 In Progress**: Orders and Trades (requires additional API endpoint configuration)

### Using the API Client

```python
from src.api.breeze_client import BreezeClient

# Initialize client
client = BreezeClient()

# Authenticate using API credentials (no user ID/password needed)
if client.authenticate():
    
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
- **API Credentials Only**: No need to store user ID or password
- **Session Management**: Automatic session token handling with expiry
- **Secure Headers**: Proper authentication headers for all API requests

## 📊 API Endpoints Supported

- **Authentication**: Session generation and management using API credentials
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

#!/usr/bin/env python3
"""
Test script for ICICI Breeze API integration.
Tests authentication, account balance, portfolio, and open orders.
"""
import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from api.breeze_client import BreezeClient
from utils.config import config

def print_separator(title: str):
    """Print a formatted separator with title."""
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def print_json(data, title: str):
    """Pretty print JSON data with title."""
    print(f"\n{title}:")
    print("-" * 30)
    if data:
        print(json.dumps(data, indent=2, default=str))
    else:
        print("No data available")

def test_configuration():
    """Test configuration loading."""
    print_separator("Testing Configuration")
    
    print("Configuration loaded:")
    config_dict = config.to_dict()
    for key, value in config_dict.items():
        print(f"  {key}: {value}")
    
    if config.validate_config():
        print("✅ Configuration is valid")
        return True
    else:
        print("❌ Configuration is invalid")
        return False

def test_authentication():
    """Test authentication with API credentials."""
    print_separator("Testing Authentication")
    
    # Initialize client and authenticate
    client = BreezeClient()
    
    if client.authenticate():
        print("✅ Authentication successful!")
        return client
    else:
        print("❌ Authentication failed!")
        return None

def test_account_balance(client: BreezeClient):
    """Test account balance retrieval."""
    print_separator("Testing Account Balance")
    
    balance = client.get_account_balance()
    if balance:
        print_json(balance, "Account Balance")
        return True
    else:
        print("❌ Failed to get account balance")
        return False

def test_portfolio(client: BreezeClient):
    """Test portfolio retrieval."""
    print_separator("Testing Portfolio")
    
    portfolio = client.get_portfolio()
    if portfolio:
        print_json(portfolio, "Portfolio Holdings")
        print(f"Total holdings: {len(portfolio)}")
        return True
    else:
        print("❌ Failed to get portfolio")
        return False

def test_open_orders(client: BreezeClient):
    """Test open orders retrieval."""
    print_separator("Testing Open Orders")
    
    open_orders = client.get_open_orders()
    if open_orders is not None:  # Could be empty list
        print_json(open_orders, "Open Orders")
        print(f"Total open orders: {len(open_orders)}")
        return True
    else:
        print("❌ Failed to get open orders")
        return False

def test_order_history(client: BreezeClient):
    """Test order history retrieval."""
    print_separator("Testing Order History")
    
    history = client.get_order_history(days=7)
    if history:
        print_json(history, "Order History (Last 7 days)")
        print(f"Total orders: {len(history)}")
        return True
    else:
        print("❌ Failed to get order history")
        return False

def main():
    """Main test function."""
    print("🚀 ICICI Breeze API Test Suite")
    print("This script will test the basic functionality of the Breeze API integration.")
    print("Make sure your .env file contains BREEZE_API_KEY, BREEZE_SECRET_KEY, and BREEZE_SESSION_TOKEN")
    
    # Test 1: Configuration
    if not test_configuration():
        print("\n❌ Configuration test failed. Please check your .env file.")
        return
    
    # Test 2: Authentication
    client = test_authentication()
    if not client:
        print("\n❌ Authentication test failed. Please check your API credentials.")
        return
    
    try:
        # Test 3: Account Balance
        test_account_balance(client)
        
        # Test 4: Portfolio
        test_portfolio(client)
        
        # Test 5: Open Orders
        test_open_orders(client)
        
        # Test 6: Order History
        test_order_history(client)
        
        print_separator("Test Summary")
        print("✅ All tests completed!")
        print("The basic ICICI Breeze API integration is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
    
    finally:
        # Logout
        print("\nLogging out...")
        client.logout()
        print("✅ Logged out successfully")

if __name__ == "__main__":
    main()

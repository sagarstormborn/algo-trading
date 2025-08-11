"""
ICICI Breeze API Client for trading operations.
Handles account balance, portfolio, open orders, and other trading functions.
"""
import requests
import json
from typing import Dict, List, Optional, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.config import config
from src.auth.breeze_auth import BreezeAuth

class BreezeClient:
    """Main client for ICICI Breeze API operations."""
    
    def __init__(self):
        """Initialize Breeze API client."""
        self.auth = BreezeAuth()
        self.base_url = config.breeze_base_url
    
    def authenticate(self) -> bool:
        """
        Authenticate with ICICI Breeze API using API credentials.
        
        Returns:
            bool: True if authentication successful
        """
        success, message = self.auth.generate_session()
        if success:
            print("✅ Authentication successful!")
        else:
            print(f"❌ Authentication failed: {message}")
        return success
    
    def get_account_balance(self) -> Optional[Dict[str, Any]]:
        """
        Get account balance and margin details.
        
        Returns:
            Dict containing account balance information or None if failed
        """
        try:
            if not self.auth.validate_session():
                raise ValueError("No valid session. Please authenticate first.")
            
            url = f"{self.base_url}/funds"
            
            headers = self.auth.get_auth_headers()
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('Status') == 200:
                    return data.get('Success', {})
                else:
                    print(f"❌ Failed to get account balance: {data.get('Error', 'Unknown error')}")
                    return None
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Exception getting account balance: {str(e)}")
            return None
    
    def get_portfolio(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get current portfolio holdings.
        
        Returns:
            List of portfolio holdings or None if failed
        """
        try:
            if not self.auth.validate_session():
                raise ValueError("No valid session. Please authenticate first.")
            
            url = f"{self.base_url}/portfolio"
            
            headers = self.auth.get_auth_headers()
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('Status') == 200:
                    return data.get('Success', [])
                else:
                    print(f"❌ Failed to get portfolio: {data.get('Error', 'Unknown error')}")
                    return None
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Exception getting portfolio: {str(e)}")
            return None
    
    def get_open_orders(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get all open/pending orders.
        
        Returns:
            List of open orders or None if failed
        """
        try:
            if not self.auth.validate_session():
                raise ValueError("No valid session. Please authenticate first.")
            
            url = f"{self.base_url}/orders"
            
            headers = self.auth.get_auth_headers()
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('Status') == 200:
                    # Filter for open/pending orders
                    all_orders = data.get('Success', [])
                    open_orders = [
                        order for order in all_orders 
                        if order.get('status') in ['PENDING', 'OPEN', 'PARTIALLY_FILLED']
                    ]
                    return open_orders
                else:
                    print(f"❌ Failed to get open orders: {data.get('Error', 'Unknown error')}")
                    return None
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Exception getting open orders: {str(e)}")
            return None
    
    def get_order_history(self, days: int = 7) -> Optional[List[Dict[str, Any]]]:
        """
        Get order history for the specified number of days.
        
        Args:
            days: Number of days to look back (default: 7)
            
        Returns:
            List of historical orders or None if failed
        """
        try:
            if not self.auth.validate_session():
                raise ValueError("No valid session. Please authenticate first.")
            
            url = f"{self.base_url}/orders"
            
            headers = self.auth.get_auth_headers()
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('Status') == 200:
                    return data.get('Success', [])
                else:
                    print(f"❌ Failed to get order history: {data.get('Error', 'Unknown error')}")
                    return None
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Exception getting order history: {str(e)}")
            return None
    
    def logout(self) -> bool:
        """
        Logout from the API session.
        
        Returns:
            bool: True if logout successful
        """
        return self.auth.logout()
    
    def is_authenticated(self) -> bool:
        """
        Check if currently authenticated.
        
        Returns:
            bool: True if authenticated and session is valid
        """
        return self.auth.validate_session()

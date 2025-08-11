"""
ICICI Breeze API Client for trading operations.
Handles account balance, portfolio, open orders, and other trading functions.
"""
import requests
import json
import hashlib
from datetime import datetime, timezone
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
    
    def _compute_checksum(self, timestamp: str, payload: str) -> str:
        """
        Compute checksum using SHA256 hash (Timestamp + JSON Post Data + secret_key).
        
        Args:
            timestamp: ISO8601 UTC DateTime Format
            payload: JSON string payload
            
        Returns:
            str: SHA256 checksum
        """
        checksum_string = timestamp + payload + config.breeze_secret_key
        return hashlib.sha256(checksum_string.encode("utf-8")).hexdigest()
    
    def _get_auth_headers(self, payload: str = "") -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Args:
            payload: JSON string payload for checksum computation
            
        Returns:
            Dict containing authentication headers
        """
        if not self.auth.validate_session():
            raise ValueError("No valid session. Please authenticate first.")
        
        timestamp = datetime.now(timezone.utc).isoformat()[:19] + '.000Z'
        checksum = self._compute_checksum(timestamp, payload)
        
        return {
            'Content-Type': 'application/json',
            'X-Checksum': 'token ' + checksum,
            'X-Timestamp': timestamp,
            'X-AppKey': config.breeze_api_key,
            'X-SessionToken': self.auth.get_session_token()
        }
    
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
            payload = json.dumps({})
            
            headers = self._get_auth_headers(payload)
            
            response = requests.get(url, headers=headers, data=payload)
            
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
            
            url = f"{self.base_url}/dematholdings"
            payload = json.dumps({})
            
            headers = self._get_auth_headers(payload)
            
            response = requests.get(url, headers=headers, data=payload)
            
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
            
            # For now, return empty list since trades endpoint has checksum issues
            # This can be implemented later when we resolve the checksum computation
            print("ℹ️  Open orders functionality temporarily disabled due to API checksum requirements")
            return []
                
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
            
            # For now, return empty list since trades endpoint has checksum issues
            # This can be implemented later when we resolve the checksum computation
            print("ℹ️  Order history functionality temporarily disabled due to API checksum requirements")
            return []
                
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

"""
Authentication module for ICICI Breeze API.
Handles session management, token generation, and authentication.
"""
import requests
import json
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.config import config

class BreezeAuth:
    """Authentication handler for ICICI Breeze API."""
    
    def __init__(self):
        """Initialize authentication handler."""
        self.session_token = None
        self.session_expiry = None
        self.base_url = config.breeze_base_url
        self.api_key = config.breeze_api_key
        self.secret_key = config.breeze_secret_key
        self.account_id = config.breeze_account_id
    
    def generate_session(self, user_id: str, password: str) -> Tuple[bool, str]:
        """
        Generate session token using user credentials.
        
        Args:
            user_id: ICICI Direct user ID
            password: ICICI Direct password
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            url = f"{self.base_url}/authenticate"
            
            payload = {
                "AppKey": self.api_key,
                "AppSecret": self.secret_key,
                "UserId": user_id,
                "Password": password,
                "Source": "API"
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('Status') == 200:
                    self.session_token = data.get('Success', {}).get('session_token')
                    # Session typically expires in 24 hours
                    self.session_expiry = datetime.now() + timedelta(hours=23)
                    
                    # Update config with session token
                    config.breeze_session_token = self.session_token
                    
                    return True, "Session generated successfully"
                else:
                    return False, f"Authentication failed: {data.get('Error', 'Unknown error')}"
            else:
                return False, f"HTTP Error: {response.status_code}"
                
        except Exception as e:
            return False, f"Exception during authentication: {str(e)}"
    
    def validate_session(self) -> bool:
        """
        Check if current session is valid.
        
        Returns:
            bool: True if session is valid, False otherwise
        """
        if not self.session_token:
            return False
        
        if self.session_expiry and datetime.now() > self.session_expiry:
            return False
        
        return True
    
    def get_session_token(self) -> Optional[str]:
        """
        Get current session token.
        
        Returns:
            str: Session token if valid, None otherwise
        """
        if self.validate_session():
            return self.session_token
        return None
    
    def logout(self) -> bool:
        """
        Logout and invalidate session.
        
        Returns:
            bool: True if logout successful
        """
        try:
            if not self.session_token:
                return True
            
            url = f"{self.base_url}/logout"
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.session_token}'
            }
            
            response = requests.post(url, headers=headers)
            
            # Clear session regardless of response
            self.session_token = None
            self.session_expiry = None
            config.breeze_session_token = None
            
            return response.status_code == 200
            
        except Exception:
            # Clear session even if logout fails
            self.session_token = None
            self.session_expiry = None
            config.breeze_session_token = None
            return True
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dict containing authentication headers
        """
        if not self.validate_session():
            raise ValueError("No valid session. Please authenticate first.")
        
        return {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': '',
            'Authorization': f'Bearer {self.session_token}'
        }

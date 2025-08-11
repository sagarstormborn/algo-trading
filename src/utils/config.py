"""
Configuration utility for loading environment variables and API settings.
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any

class Config:
    """Configuration class for managing environment variables and API settings."""
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        load_dotenv()
        self._load_config()
    
    def _load_config(self):
        """Load all configuration variables from environment."""
        self.breeze_api_key = os.getenv('BREEZE_API_KEY')
        self.breeze_secret_key = os.getenv('BREEZE_SECRET_KEY')
        self.breeze_session_token = os.getenv('BREEZE_SESSION_TOKEN')
        self.breeze_base_url = os.getenv('BREEZE_BASE_URL', 'https://api.icicidirect.com/breezeapi/v1')
        self.breeze_account_id = os.getenv('BREEZE_ACCOUNT_ID')
        self.environment = os.getenv('ENVIRONMENT', 'development')
    
    def validate_config(self) -> bool:
        """Validate that all required configuration is present."""
        required_fields = [
            'breeze_api_key',
            'breeze_secret_key', 
            'breeze_session_token',
            'breeze_account_id'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(self, field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"Missing required configuration: {', '.join(missing_fields)}")
            return False
        
        return True
    
    def get_api_headers(self) -> Dict[str, str]:
        """Get headers required for API requests."""
        return {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': '',
            'Authorization': f'Bearer {self.breeze_session_token}'
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary (excluding sensitive data)."""
        return {
            'breeze_base_url': self.breeze_base_url,
            'breeze_account_id': self.breeze_account_id,
            'environment': self.environment
        }

# Global configuration instance
config = Config()

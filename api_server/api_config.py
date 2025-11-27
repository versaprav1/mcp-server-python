"""
Configuration management for API MCP Server.
Loads API credentials from environment variables or .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class APIConfig:
    """API configuration with environment variable support."""
    
    def __init__(self):
        # API base URL
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:3000")
        
        # Remove trailing slash if present
        if self.base_url.endswith("/"):
            self.base_url = self.base_url[:-1]
        
        # Authentication method: 'bearer', 'api_key', 'basic', or 'none'
        self.auth_method = os.getenv("API_AUTH_METHOD", "bearer").lower()
        
        # Authentication credentials
        self.api_key = os.getenv("API_KEY", "")
        self.bearer_token = os.getenv("API_BEARER_TOKEN", "")
        self.basic_username = os.getenv("API_BASIC_USERNAME", "")
        self.basic_password = os.getenv("API_BASIC_PASSWORD", "")
        
        # Request timeout in seconds
        self.timeout = int(os.getenv("API_TIMEOUT", "30"))
        
        # Valid schemas
        self.valid_schemas = ["dev", "prod", "test"]
    
    def get_auth_headers(self):
        """Get authentication headers based on auth method."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if self.auth_method == "bearer" and self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        elif self.auth_method == "api_key" and self.api_key:
            headers["X-API-Key"] = self.api_key
        
        return headers
    
    def get_basic_auth(self):
        """Get basic auth credentials if configured."""
        if self.auth_method == "basic" and self.basic_username:
            return (self.basic_username, self.basic_password)
        return None
    
    def validate_schema(self, schema: str) -> bool:
        """Validate if schema is one of the allowed values."""
        return schema in self.valid_schemas


# Global config instance
api_config = APIConfig()

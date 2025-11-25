"""
HTTP client for making API requests to the integration platform.
Handles authentication, error handling, and response parsing.
"""

import requests
from typing import Optional, Dict, Any
from api_config import api_config


class APIClient:
    """HTTP client for integration platform API."""
    
    def __init__(self):
        self.base_url = api_config.base_url
        self.timeout = api_config.timeout
        self.session = requests.Session()
        self.session.headers.update(api_config.get_auth_headers())
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests
        
        Returns:
            Dictionary with response data or error information
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            # Add basic auth if configured
            basic_auth = api_config.get_basic_auth()
            if basic_auth:
                kwargs['auth'] = basic_auth
            
            # Set timeout
            kwargs.setdefault('timeout', self.timeout)
            
            response = self.session.request(method, url, **kwargs)
            
            # Check for HTTP errors
            response.raise_for_status()
            
            # Try to parse JSON response
            try:
                data = response.json()
            except ValueError:
                # If response is not JSON, return text
                data = {"text": response.text}
            
            return {
                "success": True,
                "status_code": response.status_code,
                "data": data
            }
        
        except requests.exceptions.HTTPError as e:
            error_message = str(e)
            error_detail = ""
            
            # Try to get error details from response
            try:
                if e.response is not None:
                    error_detail = e.response.json()
            except:
                if e.response is not None:
                    error_detail = e.response.text
            
            return {
                "success": False,
                "status_code": e.response.status_code if e.response else None,
                "error": error_message,
                "error_detail": error_detail
            }
        
        except requests.exceptions.ConnectionError as e:
            return {
                "success": False,
                "error": "Connection Error",
                "error_detail": f"Could not connect to {url}. Please check the API_BASE_URL and network connection."
            }
        
        except requests.exceptions.Timeout as e:
            return {
                "success": False,
                "error": "Timeout Error",
                "error_detail": f"Request to {url} timed out after {self.timeout} seconds."
            }
        
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": "Request Error",
                "error_detail": str(e)
            }
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return self._make_request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a POST request."""
        return self._make_request("POST", endpoint, json=data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a PUT request."""
        return self._make_request("PUT", endpoint, json=data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self._make_request("DELETE", endpoint)
    
    def validate_schema(self, schema: str) -> bool:
        """Validate schema parameter."""
        return api_config.validate_schema(schema)

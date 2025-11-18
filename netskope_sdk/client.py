"""
Netskope API Client
Main client for interacting with Netskope REST API v2
"""

import json
import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    NetskopeAPIError,
    AuthenticationError,
    RateLimitError,
    ValidationError
)


class NetskopeClient:
    """
    Main client for Netskope API interactions

    Args:
        tenant: Netskope tenant name (e.g., 'yourcompany')
        api_token: API token for authentication
        api_version: API version (default: 'v2')
        timeout: Request timeout in seconds (default: 30)
        max_retries: Maximum number of retry attempts (default: 3)
        enable_logging: Enable detailed logging (default: True)
    """

    def __init__(
        self,
        tenant: str,
        api_token: str,
        api_version: str = "v2",
        timeout: int = 30,
        max_retries: int = 3,
        enable_logging: bool = True
    ):
        self.tenant = tenant
        self.api_token = api_token
        self.api_version = api_version
        self.timeout = timeout
        self.base_url = f"https://{tenant}.goskope.com/api/{api_version}"

        # Set up logging
        self.logger = self._setup_logging(enable_logging)

        # Set up session with retry logic
        self.session = self._setup_session(max_retries)

        # Track API usage
        self.request_count = 0
        self.last_request_time = None

    def _setup_logging(self, enable: bool) -> logging.Logger:
        """Configure logging for API operations"""
        logger = logging.getLogger("netskope_sdk")

        if enable and not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _setup_session(self, max_retries: int) -> requests.Session:
        """Configure requests session with retry logic"""
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session

    def _get_headers(self) -> Dict[str, str]:
        """Generate request headers with authentication"""
        return {
            "Netskope-Api-Token": self.api_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        self.logger.debug(f"Response status: {response.status_code}")

        # Handle rate limiting
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            raise RateLimitError(
                f"Rate limit exceeded. Retry after {retry_after} seconds",
                status_code=429,
                response=response
            )

        # Handle authentication errors
        if response.status_code == 401:
            raise AuthenticationError(
                "Authentication failed. Check your API token.",
                status_code=401,
                response=response
            )

        # Handle other client errors
        if 400 <= response.status_code < 500:
            error_msg = f"Client error: {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get("message", error_msg)
            except json.JSONDecodeError:
                error_msg = response.text or error_msg

            raise NetskopeAPIError(
                error_msg,
                status_code=response.status_code,
                response=response
            )

        # Handle server errors
        if response.status_code >= 500:
            raise NetskopeAPIError(
                f"Server error: {response.status_code}",
                status_code=response.status_code,
                response=response
            )

        # Parse successful response
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"status": "success", "data": response.text}

    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an API request

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint (e.g., '/policy/dlp')
            data: Request body data
            params: URL query parameters

        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"

        self.logger.info(f"{method} {url}")
        self.request_count += 1
        self.last_request_time = datetime.utcnow()

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                json=data,
                params=params,
                timeout=self.timeout
            )

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise NetskopeAPIError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise NetskopeAPIError(f"Connection error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise NetskopeAPIError(f"Request failed: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request"""
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a POST request"""
        return self.request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a PUT request"""
        return self.request("PUT", endpoint, data=data)

    def patch(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a PATCH request"""
        return self.request("PATCH", endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request"""
        return self.request("DELETE", endpoint)

    def test_connection(self) -> bool:
        """
        Test API connectivity and authentication

        Returns:
            True if connection is successful
        """
        try:
            # Try to fetch basic tenant info or policies
            self.get("/status")
            self.logger.info("Connection test successful")
            return True
        except AuthenticationError:
            self.logger.error("Authentication failed")
            return False
        except NetskopeAPIError as e:
            self.logger.error(f"Connection test failed: {e}")
            return False

    def get_api_usage(self) -> Dict[str, Any]:
        """
        Get API usage statistics

        Returns:
            Dictionary with usage information
        """
        return {
            "request_count": self.request_count,
            "last_request_time": self.last_request_time.isoformat() if self.last_request_time else None,
            "tenant": self.tenant,
            "api_version": self.api_version
        }

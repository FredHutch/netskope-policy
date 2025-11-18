"""
Custom exceptions for Netskope SDK
"""


class NetskopeAPIError(Exception):
    """Base exception for all Netskope API errors"""

    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(NetskopeAPIError):
    """Raised when authentication fails"""
    pass


class PolicyNotFoundError(NetskopeAPIError):
    """Raised when a policy cannot be found"""
    pass


class ValidationError(NetskopeAPIError):
    """Raised when input validation fails"""
    pass


class RateLimitError(NetskopeAPIError):
    """Raised when API rate limit is exceeded"""
    pass


class ConfigurationError(NetskopeAPIError):
    """Raised when there's a configuration error"""
    pass

"""
Netskope SDK for Real-Time Protection API
A Python SDK for interacting with Netskope REST API v2
"""

from .client import NetskopeClient
from .policies import PolicyManager
from .dlp import DLPManager
from .threats import ThreatManager
from .exceptions import (
    NetskopeAPIError,
    AuthenticationError,
    PolicyNotFoundError,
    ValidationError
)

__version__ = "1.0.0"
__all__ = [
    "NetskopeClient",
    "PolicyManager",
    "DLPManager",
    "ThreatManager",
    "NetskopeAPIError",
    "AuthenticationError",
    "PolicyNotFoundError",
    "ValidationError"
]

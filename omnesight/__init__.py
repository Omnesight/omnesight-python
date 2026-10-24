"""
Omnesight Python SDK
Sovereign Operational Intelligence & Autonomous Execution Infrastructure
"""

from .client import Omnesight, AsyncOmnesight
from .exceptions import (
    OmnesightError,
    AuthenticationError,
    PolicyViolationError,
    RateLimitError,
    NotFoundError,
    InternalServerError
)

__version__ = "1.0.0"
__all__ = [
    "Omnesight",
    "AsyncOmnesight",
    "OmnesightError",
    "AuthenticationError",
    "PolicyViolationError",
    "RateLimitError",
    "NotFoundError",
    "InternalServerError",
]

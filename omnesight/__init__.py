"""
Omnesight Python SDK
Sovereign Operational Intelligence & Autonomous Execution Infrastructure
"""

from .client import AsyncOmnesight, Omnesight
from .exceptions import (
    AuthenticationError,
    InternalServerError,
    NotFoundError,
    OmnesightError,
    PolicyViolationError,
    RateLimitError,
)
from .models import (
    HackmalimInferRequest,
    HackmalimInferResponse,
    SandalfonChatRequest,
    SandalfonChatResponse,
    SandalfonDiscoverRequest,
    SandalfonDiscoverResponse,
)

__version__ = "1.1.0"
__all__ = [
    "AsyncOmnesight",
    "AuthenticationError",
    "HackmalimInferRequest",
    "HackmalimInferResponse",
    "InternalServerError",
    "NotFoundError",
    "Omnesight",
    "OmnesightError",
    "PolicyViolationError",
    "RateLimitError",
    "SandalfonChatRequest",
    "SandalfonChatResponse",
    "SandalfonDiscoverRequest",
    "SandalfonDiscoverResponse",
]

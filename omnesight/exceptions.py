"""
Omnesight SDK Exceptions
"""

class OmnesightError(Exception):
    """Base exception for all Omnesight SDK errors."""
    def __init__(self, message: str, status_code: int = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

class AuthenticationError(OmnesightError):
    """Raised when the provided API key or cryptographic token is invalid or expired."""
    pass

class PolicyViolationError(OmnesightError):
    """Raised when an action violates enterprise governance, policy limits, or requires escalation."""
    pass

class RateLimitError(OmnesightError):
    """Raised when telemetry throughput exceeds contracted tier rate limits."""
    pass

class NotFoundError(OmnesightError):
    """Raised when a requested entity, pipeline, or action does not exist."""
    pass

class InternalServerError(OmnesightError):
    """Raised when the sovereign backend encounters an unhandled infrastructure error."""
    pass

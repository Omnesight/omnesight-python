"""
Omnesight Client Implementation
Supports synchronous and asynchronous execution, enterprise custom endpoints (VPC),
and automatic exponential backoff retries.
"""

from typing import Optional, Dict, Any
import os
import httpx
from .exceptions import (
    OmnesightError,
    AuthenticationError,
    PolicyViolationError,
    RateLimitError,
    NotFoundError,
    InternalServerError
)
from .resources.telemetry import TelemetryResource, AsyncTelemetryResource
from .resources.reconciliation import ReconciliationResource, AsyncReconciliationResource
from .resources.actions import ActionsResource, AsyncActionsResource

class Omnesight:
    """
    Synchronous enterprise client for Omnesight Operational Intelligence Infrastructure.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        self.api_key = api_key or os.environ.get("OMNESIGHT_API_KEY")
        if not self.api_key:
            raise AuthenticationError("API key must be provided or set via OMNESIGHT_API_KEY environment variable.")
        
        resolved_base_url = base_url or os.environ.get("OMNESIGHT_BASE_URL")
        if not resolved_base_url:
            raise OmnesightError(
                "Endpoint base_url must be specified or set via OMNESIGHT_BASE_URL "
                "(e.g. your enterprise VPC or dedicated sovereign gateway)."
            )
        self.base_url = resolved_base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        
        self._http_client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "omnesight-python-sdk/1.0.0"
            },
            timeout=self.timeout
        )

        # Resources
        self.telemetry = TelemetryResource(self)
        self.reconciliation = ReconciliationResource(self)
        self.actions = ActionsResource(self)

    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        for attempt in range(self.max_retries + 1):
            try:
                resp = self._http_client.request(method, path, **kwargs)
                return self._handle_response(resp)
            except httpx.TransportError as e:
                if attempt == self.max_retries:
                    raise InternalServerError(f"Connection to Omnesight infrastructure failed: {str(e)}")

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        if 200 <= response.status_code < 300:
            return response.json()
        
        error_msg = response.text
        try:
            error_data = response.json()
            error_msg = error_data.get("message", error_data.get("detail", error_msg))
        except Exception:
            pass

        if response.status_code == 401 or response.status_code == 403:
            raise AuthenticationError(error_msg, status_code=response.status_code)
        elif response.status_code == 422:
            raise PolicyViolationError(error_msg, status_code=response.status_code)
        elif response.status_code == 429:
            raise RateLimitError(error_msg, status_code=response.status_code)
        elif response.status_code == 404:
            raise NotFoundError(error_msg, status_code=response.status_code)
        else:
            raise InternalServerError(error_msg, status_code=response.status_code)

    def close(self):
        self._http_client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncOmnesight:
    """
    Asynchronous enterprise client for Omnesight Operational Intelligence Infrastructure.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        self.api_key = api_key or os.environ.get("OMNESIGHT_API_KEY")
        if not self.api_key:
            raise AuthenticationError("API key must be provided or set via OMNESIGHT_API_KEY environment variable.")
        
        resolved_base_url = base_url or os.environ.get("OMNESIGHT_BASE_URL")
        if not resolved_base_url:
            raise OmnesightError(
                "Endpoint base_url must be specified or set via OMNESIGHT_BASE_URL "
                "(e.g. your enterprise VPC or dedicated sovereign gateway)."
            )
        self.base_url = resolved_base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

        self._http_client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "omnesight-python-sdk/1.0.0"
            },
            timeout=self.timeout
        )

        self.telemetry = AsyncTelemetryResource(self)
        self.reconciliation = AsyncReconciliationResource(self)
        self.actions = AsyncActionsResource(self)

    async def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        for attempt in range(self.max_retries + 1):
            try:
                resp = await self._http_client.request(method, path, **kwargs)
                return self._handle_response(resp)
            except httpx.TransportError as e:
                if attempt == self.max_retries:
                    raise InternalServerError(f"Connection to Omnesight infrastructure failed: {str(e)}")

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        if 200 <= response.status_code < 300:
            return response.json()
        
        error_msg = response.text
        try:
            error_data = response.json()
            error_msg = error_data.get("message", error_data.get("detail", error_msg))
        except Exception:
            pass

        if response.status_code in (401, 403):
            raise AuthenticationError(error_msg, status_code=response.status_code)
        elif response.status_code == 422:
            raise PolicyViolationError(error_msg, status_code=response.status_code)
        elif response.status_code == 429:
            raise RateLimitError(error_msg, status_code=response.status_code)
        elif response.status_code == 404:
            raise NotFoundError(error_msg, status_code=response.status_code)
        else:
            raise InternalServerError(error_msg, status_code=response.status_code)

    async def aclose(self):
        await self._http_client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()

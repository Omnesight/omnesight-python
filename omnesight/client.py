"""
Omnesight Client Implementation
Supports synchronous and asynchronous execution, sovereign MLOps gateways,
custom VPC endpoints, and automatic transport retries.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from .exceptions import (
    AuthenticationError,
    InternalServerError,
    NotFoundError,
    OmnesightError,
    PolicyViolationError,
    RateLimitError,
)
from .resources.actions import ActionsResource, AsyncActionsResource
from .resources.hackmalim import AsyncHackmalimResource, HackmalimResource
from .resources.reconciliation import (
    AsyncReconciliationResource,
    ReconciliationResource,
)
from .resources.sandalfon import AsyncSandalfonResource, SandalfonResource
from .resources.telemetry import AsyncTelemetryResource, TelemetryResource

DEFAULT_BASE_URL = "http://127.0.0.1:8001"
SDK_USER_AGENT = "omnesight-python-sdk/1.1.0"

_STATUS_EXCEPTIONS = {
    401: AuthenticationError,
    403: AuthenticationError,
    404: NotFoundError,
    422: PolicyViolationError,
    429: RateLimitError,
}


def _resolve_client_settings(
    api_key: str | None,
    base_url: str | None,
) -> tuple[str, str, dict[str, str]]:
    """Resolve API credentials, gateway base URL, and standard Omnesight headers."""
    resolved_key = api_key or os.environ.get("OMNESIGHT_API_KEY")
    if not resolved_key:
        raise AuthenticationError(
            "API key must be provided or set via OMNESIGHT_API_KEY environment variable."
        )
    env_url = os.environ.get("OMNESIGHT_BASE_URL")
    resolved_url = (base_url or env_url or DEFAULT_BASE_URL).rstrip("/")
    headers = {
        "Authorization": f"Bearer {resolved_key}",
        "X-API-Key": resolved_key,
        "Content-Type": "application/json",
        "User-Agent": SDK_USER_AGENT,
    }
    return resolved_key, resolved_url, headers


def _parse_response(response: httpx.Response) -> dict[str, Any]:
    """Decode successful JSON payloads or raise the typed Omnesight SDK exception."""
    if 200 <= response.status_code < 300:
        return response.json()

    error_msg = response.text
    try:
        error_data = response.json()
        error_msg = error_data.get("message", error_data.get("detail", error_msg))
    except ValueError:
        error_msg = response.text

    exc_cls = _STATUS_EXCEPTIONS.get(response.status_code, InternalServerError)
    raise exc_cls(error_msg, status_code=response.status_code)


class Omnesight:
    """Synchronous enterprise client for Omnesight Sovereign MLOps Infrastructure."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        transport: httpx.BaseTransport | None = None,
    ):
        resolved = _resolve_client_settings(api_key, base_url)
        self.api_key, self.base_url, headers = resolved
        self.timeout = timeout
        self.max_retries = max_retries

        client_kwargs: dict[str, Any] = {
            "base_url": self.base_url,
            "headers": headers,
            "timeout": self.timeout,
        }
        if transport is not None:
            client_kwargs["transport"] = transport
        self._http_client = httpx.Client(**client_kwargs)

        self.telemetry = TelemetryResource(self)
        self.reconciliation = ReconciliationResource(self)
        self.actions = ActionsResource(self)
        self.hackmalim = HackmalimResource(self)
        self.sandalfon = SandalfonResource(self)

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        for attempt in range(self.max_retries + 1):
            try:
                resp = self._http_client.request(method, path, **kwargs)
                return _parse_response(resp)
            except httpx.TransportError as exc:
                if attempt == self.max_retries:
                    msg = f"Connection to Omnesight infrastructure failed: {exc}"
                    raise InternalServerError(msg) from exc
        raise OmnesightError("Request failed after retries.")

    def close(self):
        self._http_client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncOmnesight:
    """Asynchronous enterprise client for Omnesight Sovereign MLOps Infrastructure."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        resolved = _resolve_client_settings(api_key, base_url)
        self.api_key, self.base_url, headers = resolved
        self.timeout = timeout
        self.max_retries = max_retries

        client_kwargs: dict[str, Any] = {
            "base_url": self.base_url,
            "headers": headers,
            "timeout": self.timeout,
        }
        if transport is not None:
            client_kwargs["transport"] = transport
        self._http_client = httpx.AsyncClient(**client_kwargs)

        self.telemetry = AsyncTelemetryResource(self)
        self.reconciliation = AsyncReconciliationResource(self)
        self.actions = AsyncActionsResource(self)
        self.hackmalim = AsyncHackmalimResource(self)
        self.sandalfon = AsyncSandalfonResource(self)

    async def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        for attempt in range(self.max_retries + 1):
            try:
                resp = await self._http_client.request(method, path, **kwargs)
                return _parse_response(resp)
            except httpx.TransportError as exc:
                if attempt == self.max_retries:
                    msg = f"Connection to Omnesight infrastructure failed: {exc}"
                    raise InternalServerError(msg) from exc
        raise OmnesightError("Request failed after retries.")

    async def aclose(self):
        await self._http_client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()

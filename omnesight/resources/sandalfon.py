"""
Sandalfon v1.0 Scientific Equation Discovery & Spectral AI Engine Resource
SINDy Sparse Discovery (STLSQ) + FFT Spectral Precursor Explorer + Popperian Test.
"""

from __future__ import annotations

from typing import Any, Literal

from ..models import (
    SandalfonChatRequest,
    SandalfonChatResponse,
    SandalfonDiscoverRequest,
    SandalfonDiscoverResponse,
)

SandalfonPreset = Literal["coupled_oscillator", "predator_prey_grid", "thermal_runaway"]


class SandalfonResource:
    """Synchronous client resource for Sandalfon v1.0."""

    def __init__(self, client):
        self._client = client

    def info(self) -> dict[str, Any]:
        """Retrieve Sandalfon v1.0 model card and candidate monomial library."""
        return self._client._request("GET", "/api/v1/sandalfon/info")

    def discover(
        self,
        preset: SandalfonPreset = "coupled_oscillator",
        noise_level: float = 0.02,
        sparsity_threshold: float = 0.10,
        precursor_amp: float = 0.18,
        hypothesis_text: str | None = None,
    ) -> SandalfonDiscoverResponse:
        """Discover sparse ODEs, FFT wave precursors, and Popperian significance."""
        req = SandalfonDiscoverRequest(
            preset=preset,
            noise_level=noise_level,
            sparsity_threshold=sparsity_threshold,
            precursor_amp=precursor_amp,
            hypothesis_text=hypothesis_text,
        )
        res = self._client._request(
            "POST", "/api/v1/sandalfon/discover", json=req.model_dump()
        )
        return SandalfonDiscoverResponse(**res)

    def chat(
        self,
        message: str,
        preset: SandalfonPreset = "coupled_oscillator",
        noise_level: float = 0.02,
        sparsity_threshold: float = 0.10,
        precursor_amp: float = 0.18,
    ) -> SandalfonChatResponse:
        """Interact in natural language with Sandalfon to test hypotheses."""
        req = SandalfonChatRequest(
            message=message,
            preset=preset,
            noise_level=noise_level,
            sparsity_threshold=sparsity_threshold,
            precursor_amp=precursor_amp,
        )
        res = self._client._request(
            "POST", "/api/v1/sandalfon/chat", json=req.model_dump()
        )
        return SandalfonChatResponse(**res)


class AsyncSandalfonResource:
    """Asynchronous client resource for Sandalfon v1.0."""

    def __init__(self, client):
        self._client = client

    async def info(self) -> dict[str, Any]:
        """Retrieve Sandalfon v1.0 model card asynchronously."""
        return await self._client._request("GET", "/api/v1/sandalfon/info")

    async def discover(
        self,
        preset: SandalfonPreset = "coupled_oscillator",
        noise_level: float = 0.02,
        sparsity_threshold: float = 0.10,
        precursor_amp: float = 0.18,
        hypothesis_text: str | None = None,
    ) -> SandalfonDiscoverResponse:
        """Discover sparse ODEs and spectral precursors asynchronously."""
        req = SandalfonDiscoverRequest(
            preset=preset,
            noise_level=noise_level,
            sparsity_threshold=sparsity_threshold,
            precursor_amp=precursor_amp,
            hypothesis_text=hypothesis_text,
        )
        res = await self._client._request(
            "POST", "/api/v1/sandalfon/discover", json=req.model_dump()
        )
        return SandalfonDiscoverResponse(**res)

    async def chat(
        self,
        message: str,
        preset: SandalfonPreset = "coupled_oscillator",
        noise_level: float = 0.02,
        sparsity_threshold: float = 0.10,
        precursor_amp: float = 0.18,
    ) -> SandalfonChatResponse:
        """Query Sandalfon research dialogue asynchronously."""
        req = SandalfonChatRequest(
            message=message,
            preset=preset,
            noise_level=noise_level,
            sparsity_threshold=sparsity_threshold,
            precursor_amp=precursor_amp,
        )
        res = await self._client._request(
            "POST", "/api/v1/sandalfon/chat", json=req.model_dump()
        )
        return SandalfonChatResponse(**res)

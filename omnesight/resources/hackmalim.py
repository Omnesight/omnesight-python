"""
Hackmalim v1.0 Sovereign Non-LLM Engine Resource
Continuous-Time Liquid Neural ODE + Physics-Informed GNN + Causal SAT Verifier.
"""

from __future__ import annotations

from typing import Any

from ..models import HackmalimInferRequest, HackmalimInferResponse


class HackmalimResource:
    """Synchronous client resource for Hackmalim v1.0."""

    def __init__(self, client):
        self._client = client

    def info(self) -> dict[str, Any]:
        """Retrieve Hackmalim v1.0 model card, parameter counts, and layer metrics."""
        return self._client._request("GET", "/api/v1/hackmalim/info")

    def infer(
        self,
        shock_amplitude: float = 1.45,
        jitter_severity: float = 1.0,
        inlet_n0: float = 60.0,
        inlet_n1: float = 50.0,
        leak_node: int = 2,
        leak_magnitude: float = 22.5,
        p_max_kw: float = 55.0,
        t_max_c: float = 72.0,
        autonomous_budget_usd: float = 4200.0,
    ) -> HackmalimInferResponse:
        """Run full closed-loop 3-layer inference with EnterpriseGuardrailsEngine."""
        req = HackmalimInferRequest(
            shock_amplitude=shock_amplitude,
            jitter_severity=jitter_severity,
            inlet_n0=inlet_n0,
            inlet_n1=inlet_n1,
            leak_node=leak_node,
            leak_magnitude=leak_magnitude,
            p_max_kw=p_max_kw,
            t_max_c=t_max_c,
            autonomous_budget_usd=autonomous_budget_usd,
        )
        res = self._client._request(
            "POST", "/api/v1/hackmalim/infer", json=req.model_dump()
        )
        return HackmalimInferResponse(**res)

    def liquid(
        self,
        shock_idx: int = 160,
        shock_amplitude: float = 1.45,
        jitter_severity: float = 1.0,
    ) -> dict[str, Any]:
        """Run Layer 1 Continuous-Time Liquid Neural ODE shock detection."""
        payload = {
            "shock_idx": shock_idx,
            "shock_amplitude": shock_amplitude,
            "jitter_severity": jitter_severity,
        }
        return self._client._request("POST", "/api/v1/hackmalim/liquid", json=payload)

    def pignn(
        self,
        inlet_n0: float = 60.0,
        inlet_n1: float = 50.0,
        leak_node: int = 2,
        leak_magnitude: float = 22.5,
    ) -> dict[str, Any]:
        """Run Layer 2 Kirchhoff PI-GNN flow reconstruction and leak pinpointing."""
        payload = {
            "inlet_n0": inlet_n0,
            "inlet_n1": inlet_n1,
            "leak_node": leak_node,
            "leak_magnitude": leak_magnitude,
        }
        return self._client._request("POST", "/api/v1/hackmalim/pignn", json=payload)

    def causal(
        self,
        z_load_shift: float = 0.0,
        stress_z: float = 0.95,
        p_max_kw: float = 55.0,
        t_max_c: float = 72.0,
        neural_proposal: tuple[int, int, int, int] | None = None,
    ) -> dict[str, Any]:
        """Run Layer 3 Pearl Do-Calculus backdoor adjustment and SAT axiom verifier."""
        payload: dict[str, Any] = {
            "z_load_shift": z_load_shift,
            "stress_z": stress_z,
            "p_max_kw": p_max_kw,
            "t_max_c": t_max_c,
        }
        if neural_proposal is not None:
            payload["neural_proposal"] = list(neural_proposal)
        return self._client._request("POST", "/api/v1/hackmalim/causal", json=payload)


class AsyncHackmalimResource:
    """Asynchronous client resource for Hackmalim v1.0."""

    def __init__(self, client):
        self._client = client

    async def info(self) -> dict[str, Any]:
        """Retrieve Hackmalim v1.0 model card asynchronously."""
        return await self._client._request("GET", "/api/v1/hackmalim/info")

    async def infer(
        self,
        shock_amplitude: float = 1.45,
        jitter_severity: float = 1.0,
        inlet_n0: float = 60.0,
        inlet_n1: float = 50.0,
        leak_node: int = 2,
        leak_magnitude: float = 22.5,
        p_max_kw: float = 55.0,
        t_max_c: float = 72.0,
        autonomous_budget_usd: float = 4200.0,
    ) -> HackmalimInferResponse:
        """Run closed-loop 3-layer Hackmalim inference asynchronously."""
        req = HackmalimInferRequest(
            shock_amplitude=shock_amplitude,
            jitter_severity=jitter_severity,
            inlet_n0=inlet_n0,
            inlet_n1=inlet_n1,
            leak_node=leak_node,
            leak_magnitude=leak_magnitude,
            p_max_kw=p_max_kw,
            t_max_c=t_max_c,
            autonomous_budget_usd=autonomous_budget_usd,
        )
        res = await self._client._request(
            "POST", "/api/v1/hackmalim/infer", json=req.model_dump()
        )
        return HackmalimInferResponse(**res)

    async def liquid(
        self,
        shock_idx: int = 160,
        shock_amplitude: float = 1.45,
        jitter_severity: float = 1.0,
    ) -> dict[str, Any]:
        """Run Layer 1 Liquid ODE inference asynchronously."""
        payload = {
            "shock_idx": shock_idx,
            "shock_amplitude": shock_amplitude,
            "jitter_severity": jitter_severity,
        }
        return await self._client._request(
            "POST", "/api/v1/hackmalim/liquid", json=payload
        )

    async def pignn(
        self,
        inlet_n0: float = 60.0,
        inlet_n1: float = 50.0,
        leak_node: int = 2,
        leak_magnitude: float = 22.5,
    ) -> dict[str, Any]:
        """Run Layer 2 PI-GNN inference asynchronously."""
        payload = {
            "inlet_n0": inlet_n0,
            "inlet_n1": inlet_n1,
            "leak_node": leak_node,
            "leak_magnitude": leak_magnitude,
        }
        return await self._client._request(
            "POST", "/api/v1/hackmalim/pignn", json=payload
        )

    async def causal(
        self,
        z_load_shift: float = 0.0,
        stress_z: float = 0.95,
        p_max_kw: float = 55.0,
        t_max_c: float = 72.0,
        neural_proposal: tuple[int, int, int, int] | None = None,
    ) -> dict[str, Any]:
        """Run Layer 3 Pearl Do-Calculus + SAT verifier asynchronously."""
        payload: dict[str, Any] = {
            "z_load_shift": z_load_shift,
            "stress_z": stress_z,
            "p_max_kw": p_max_kw,
            "t_max_c": t_max_c,
        }
        if neural_proposal is not None:
            payload["neural_proposal"] = list(neural_proposal)
        return await self._client._request(
            "POST", "/api/v1/hackmalim/causal", json=payload
        )

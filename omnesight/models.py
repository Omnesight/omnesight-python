"""
Omnesight SDK Models & Schemas (Pydantic v2)
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class TelemetryRecord(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    device_id: str
    metric: str
    value: float
    unit: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TelemetryIngestResponse(BaseModel):
    batch_id: str
    records_received: int
    records_committed: int
    duration_ms: float
    status: str


class DiscrepancyReport(BaseModel):
    discrepancy_id: str
    entity_a_type: str
    entity_a_id: str
    entity_b_type: str
    entity_b_id: str
    variance_amount_usd: float
    variance_pct: float
    status: str
    detected_at: datetime
    recommended_action_id: str | None = None


class ActionApprovalRequest(BaseModel):
    action_id: str
    action_type: str
    target_entity: str
    decision: str  # "APPROVE" | "REJECT" | "MODIFIED"
    supervisor_id: str
    supervisor_notes: str | None = None


class ActionStatusResponse(BaseModel):
    action_id: str
    state: str  # "PROPOSED", "SUPERVISED_APPROVAL", "COMMITTED", "REVERTED"
    action_type: str
    financial_impact_usd: float
    sha256_audit_hash: str
    executed_at: datetime | None = None


class HackmalimInferRequest(BaseModel):
    """Request payload for Hackmalim v1.0 closed-loop 3-layer inference."""

    shock_amplitude: float = Field(default=1.45, ge=0.0, le=5.0)
    jitter_severity: float = Field(default=1.0, ge=0.0, le=2.0)
    inlet_n0: float = Field(default=60.0, ge=10.0, le=150.0)
    inlet_n1: float = Field(default=50.0, ge=10.0, le=150.0)
    leak_node: int = Field(default=2, ge=1, le=5)
    leak_magnitude: float = Field(default=22.5, ge=0.0, le=50.0)
    p_max_kw: float = Field(default=55.0, ge=10.0, le=200.0)
    t_max_c: float = Field(default=72.0, ge=30.0, le=130.0)
    autonomous_budget_usd: float = Field(default=4200.0, ge=0.0, le=1_000_000.0)


class HackmalimInferResponse(BaseModel):
    """Closed-loop response from Hackmalim v1.0 sovereign inference."""

    model_config = ConfigDict(extra="allow")

    model: str
    version: str
    latency_ms: float | None = None
    inference_latency_ms: float | None = None
    computed_stress_z: float | None = None
    target_entity_id: str | None = None
    liquid_ode: dict[str, Any] | None = None
    stage_1_liquid_ode: dict[str, Any] | None = None
    pignn: dict[str, Any] | None = None
    stage_2_pignn: dict[str, Any] | None = None
    causal: dict[str, Any] | None = None
    stage_3_causal_symbolic: dict[str, Any] | None = None
    action_policy: dict[str, Any] | None = None
    guardrails: dict[str, Any] | None = None
    enterprise_guardrail: dict[str, Any] | None = None


class SandalfonDiscoverRequest(BaseModel):
    """Request payload for Sandalfon v1.0 SINDy + FFT + Popperian discovery."""

    preset: Literal[
        "coupled_oscillator",
        "predator_prey_grid",
        "thermal_runaway",
    ] = "coupled_oscillator"
    noise_level: float = Field(default=0.02, ge=0.0, le=0.20)
    sparsity_threshold: float = Field(default=0.10, ge=0.001, le=1.0)
    precursor_amp: float = Field(default=0.18, ge=0.0, le=1.0)
    hypothesis_text: str | None = Field(default=None, max_length=1000)


class SandalfonDiscoverResponse(BaseModel):
    """Response payload with discovered ODEs, FFT spectrum, and Popperian p-value."""

    model_config = ConfigDict(extra="allow")

    model: str
    version: str
    latency_ms: float
    hypothesis_text: str
    sindy: dict[str, Any]
    spectrum: dict[str, Any]
    hypothesis_test: dict[str, Any]
    discovery_proof_sha256: str


class SandalfonChatRequest(BaseModel):
    """Conversational scientific research hypothesis payload for Sandalfon v1.0."""

    message: str = Field(..., min_length=1, max_length=2000)
    preset: Literal[
        "coupled_oscillator",
        "predator_prey_grid",
        "thermal_runaway",
    ] = "coupled_oscillator"
    noise_level: float = Field(default=0.02, ge=0.0, le=0.20)
    sparsity_threshold: float = Field(default=0.10, ge=0.001, le=1.0)
    precursor_amp: float = Field(default=0.18, ge=0.0, le=1.0)


class SandalfonChatResponse(BaseModel):
    """Structured scientific response with spoken explanation and verified SINDy run."""

    model_config = ConfigDict(extra="allow")

    model: str
    version: str
    query: str | None = None
    preset_used: str | None = None
    parameters_used: dict[str, Any] | None = None
    applied_controls: dict[str, Any] | None = None
    spoken_reply: str
    voice_lang: str | None = "fr-FR"
    experiment: dict[str, Any] | None = None
    sindy: dict[str, Any] | None = None
    spectrum: dict[str, Any] | None = None
    hypothesis_test: dict[str, Any] | None = None
    discovery_proof_sha256: str | None = None

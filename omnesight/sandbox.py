"""
Omnesight SDK Sandbox & Deterministic Simulation Engine
Provides local in-memory mock transports and sandbox environments for testing,
demos, and enterprise evaluation without requiring production API keys or external networks.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
import httpx

SANDBOX_BASE_URL = "https://sandbox.omnesight.com"
DEFAULT_SANDBOX_TOKEN = "omne_sandbox_local_token"


def _build_sandbox_mock_response(request: httpx.Request) -> httpx.Response:
    """Route incoming request paths to deterministic, schema-compliant sandbox responses."""
    path = request.url.path.rstrip("/")
    method = request.method.upper()

    now_iso = datetime.now(timezone.utc).isoformat()

    # 1. Hackmalim info
    if method == "GET" and path == "/api/v1/hackmalim/info":
        return httpx.Response(
            200,
            json={
                "model": "hackmalim-v1.0",
                "version": "1.0.0-sandbox",
                "environment": "Omnesight Local Sandbox",
                "layers": [
                    "Continuous-Time Liquid Neural ODE (Neural Ordinary Differential Equations)",
                    "Physics-Informed GNN (Kirchhoff conservation laws)",
                    "Causal Symbolic SAT Verifier (deterministic guardrails)",
                ],
                "parameters_total": 14_250_000,
                "status": "SANDBOX_ACTIVE",
            },
        )

    # 2. Hackmalim inference
    if method == "POST" and path == "/api/v1/hackmalim/infer":
        body = json.loads(request.content) if request.content else {}
        shock = body.get("shock_amplitude", 1.45)
        leak_node = body.get("leak_node", 2)
        return httpx.Response(
            200,
            json={
                "model": "hackmalim-v1.0",
                "version": "1.0.0",
                "latency_ms": 0.85,
                "inference_latency_ms": 0.85,
                "computed_stress_z": 2.41,
                "target_entity_id": f"OMNE-SBX-NODE-0{leak_node}",
                "liquid_ode": {
                    "status": "STABLE",
                    "shock_dissipated": True,
                    "energy_residual_joules": 142.50,
                    "trajectory_timesteps": 50,
                },
                "stage_1_liquid_ode": {"state": "CONVERGED"},
                "pignn": {
                    "pinpointed_node": leak_node,
                    "confidence_score": 0.9984,
                    "leak_detected": True,
                    "pressure_drop_pct": 14.8,
                },
                "stage_2_pignn": {"pinpointed_node": leak_node},
                "causal": {
                    "satisfiable": True,
                    "policy_violations_count": 0,
                    "mitigation_action": "DIVERT_FLOW_NODE_04",
                },
                "stage_3_causal_symbolic": {"verified": True},
                "action_policy": {
                    "policy_id": "SAP-RULE-AUTO-401",
                    "decision": "EXECUTE_AUTONOMOUS_INTERVENTION",
                },
                "guardrails": {
                    "is_approved": True,
                    "financial_exposure_usd": 0.0,
                    "safety_compliance": "APPROVED",
                },
                "enterprise_guardrail": {
                    "is_approved": True,
                    "safety_compliance": "APPROVED",
                },
            },
        )

    # 3. Sandalfon discovery
    if method == "POST" and path == "/api/v1/sandalfon/discover":
        body = json.loads(request.content) if request.content else {}
        hypothesis = body.get("hypothesis_text") or "Sandbox differential equation discovery"
        preset = body.get("preset", "thermal_runaway")
        return httpx.Response(
            200,
            json={
                "model": "sandalfon-v1.0",
                "version": "1.0.0",
                "latency_ms": 1.15,
                "hypothesis_text": hypothesis,
                "sindy": {
                    "discovered_eq_x": "dx/dt = -0.854*x + 1.201*y - 0.042*x^3",
                    "discovered_eq_y": "dy/dt = -1.140*x - 0.312*y + 0.015*x*y",
                    "sparsity_score": 0.92,
                    "r2_fit": 0.9982,
                },
                "spectrum": {
                    "precursor_snr_db": 18.42,
                    "dominant_frequency_hz": 60.05,
                    "harmonics_detected": [120.1, 180.2],
                    "spectral_entropy": 0.142,
                },
                "hypothesis_test": {
                    "z_score": 4.18,
                    "p_value": 0.000029,
                    "is_falsified": False,
                    "falsification_verdict": "HYPOTHESIS_CONFIRMED_STATISTICALLY_SIGNIFICANT",
                },
                "discovery_proof_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            },
        )

    # 4. Sandalfon chat
    if method == "POST" and path == "/api/v1/sandalfon/chat":
        body = json.loads(request.content) if request.content else {}
        msg = body.get("message", "")
        return httpx.Response(
            200,
            json={
                "model": "sandalfon-v1.0",
                "version": "1.0.0",
                "query": msg,
                "preset_used": body.get("preset", "thermal_runaway"),
                "spoken_reply": (
                    "[Sandbox] Sandalfon scientific engine analysis: The operational telemetry "
                    "confirms stable convergence. SINDy sparse discovery identified harmonic damping "
                    "and Popperian falsification tests reject the null hypothesis (p < 0.001)."
                ),
                "voice_lang": "en-US",
                "sindy": {"discovered_eq_x": "dx/dt = -0.854*x + 1.201*y"},
                "spectrum": {"precursor_snr_db": 18.42},
                "hypothesis_test": {"z_score": 4.18, "is_falsified": False},
                "discovery_proof_sha256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
            },
        )

    # 5. Telemetry ingestion
    if method == "POST" and path == "/api/v1/telemetry/ingest":
        body = json.loads(request.content) if request.content else {}
        records = body.get("records", [])
        return httpx.Response(
            200,
            json={
                "batch_id": f"sbx_batch_{int(datetime.now().timestamp())}",
                "records_received": len(records),
                "records_committed": len(records),
                "duration_ms": 0.42,
                "status": "COMMITTED_SANDBOX",
            },
        )

    # 6. Reconciliation discrepancies
    if method == "GET" and "/api/v1/reconciliation/discrepancies" in path:
        return httpx.Response(
            200,
            json={
                "discrepancies": [
                    {
                        "discrepancy_id": "DISC-SBX-001",
                        "entity_a_type": "GIM_UEMOA_SWITCH",
                        "entity_a_id": "TX_20261116_09823",
                        "entity_b_type": "CORE_BANKING_AMPLITUDE",
                        "entity_b_id": "GL_ACCOUNT_471100",
                        "variance_amount_usd": 1450.00,
                        "variance_pct": 1.45,
                        "status": "FLAGGED_AUTO_RECONCILED",
                        "detected_at": now_iso,
                        "recommended_action_id": "ACT-SBX-001",
                    },
                    {
                        "discrepancy_id": "DISC-SBX-002",
                        "entity_a_type": "TELECOM_CDR_STREAM",
                        "entity_a_id": "CDR_MSISDN_221701234447",
                        "entity_b_type": "MOBILE_MONEY_FLOAT",
                        "entity_b_id": "WALLET_FLOAT_RECON",
                        "variance_amount_usd": 28.50,
                        "variance_pct": 0.02,
                        "status": "RESOLVED_CRYPTOGRAPHICALLY",
                        "detected_at": now_iso,
                        "recommended_action_id": "ACT-SBX-002",
                    },
                ]
            },
        )

    # 7. Action status
    if method == "GET" and "/api/v1/actions/" in path:
        action_id = path.split("/")[-1]
        return httpx.Response(
            200,
            json={
                "action_id": action_id,
                "state": "SUPERVISED_APPROVAL",
                "action_type": "LEDGER_SUSPENSE_CLEAR",
                "financial_impact_usd": 1450.00,
                "sha256_audit_hash": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
                "executed_at": now_iso,
            },
        )

    # 8. Action decision
    if method == "POST" and "/api/v1/actions/" in path and path.endswith("/decision"):
        parts = path.split("/")
        action_id = parts[-2]
        return httpx.Response(
            200,
            json={
                "action_id": action_id,
                "state": "COMMITTED",
                "action_type": "LEDGER_SUSPENSE_CLEAR",
                "financial_impact_usd": 1450.00,
                "sha256_audit_hash": "b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef01a",
                "executed_at": now_iso,
            },
        )

    # Fallback default
    return httpx.Response(200, json={"status": "ok", "sandbox": True, "path": path})


def create_sandbox_transport() -> httpx.MockTransport:
    """Create an in-memory MockTransport providing full offline simulation for the SDK."""
    return httpx.MockTransport(_build_sandbox_mock_response)

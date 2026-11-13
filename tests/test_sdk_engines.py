"""Unit tests for Omnesight Python SDK sovereign engine resources."""

import json

import httpx
import pytest

from omnesight import (
    AsyncOmnesight,
    AuthenticationError,
    HackmalimInferResponse,
    Omnesight,
    SandalfonChatResponse,
    SandalfonDiscoverResponse,
)


def _mock_handler(captured_headers: list[httpx.Headers]):
    def handler(request: httpx.Request) -> httpx.Response:
        captured_headers.append(request.headers)
        if request.headers.get("X-API-Key") == "omne_live_forbidden":
            return httpx.Response(403, json={"detail": "Model ACL denied."})

        path = request.url.path
        if path == "/api/v1/hackmalim/infer":
            return httpx.Response(
                200,
                json={
                    "model": "Hackmalim",
                    "version": "1.0.0",
                    "inference_latency_ms": 4.2,
                    "target_entity_id": "NODE_2_ACTUATOR_CLUSTER",
                    "stage_1_liquid_ode": {"shock_detected": True, "gain_pct": 89.4},
                    "stage_2_pignn": {"pinpointed_node": 2, "cons_reduction_pct": 94.1},
                    "stage_3_causal_symbolic": {
                        "pearl_do_calculus": -0.301,
                        "unsafe_states_rejected": 11,
                    },
                    "enterprise_guardrail": {
                        "is_approved": True,
                        "requires_human_review": False,
                    },
                },
            )
        if path == "/api/v1/sandalfon/discover":
            return httpx.Response(
                200,
                json={
                    "model": "Sandalfon",
                    "version": "1.0.0",
                    "latency_ms": 6.1,
                    "hypothesis_text": "Test harmonic precursor",
                    "sindy": {
                        "discovered_eq_x": "dx/dt = -0.150*x + 2.000*y",
                        "exact_support_match": True,
                    },
                    "spectrum": {
                        "precursor_hz": 11.5,
                        "precursor_snr_db": 28.1,
                        "precursor_detected": True,
                    },
                    "hypothesis_test": {
                        "r2_observed": 0.961,
                        "z_score": 49.8,
                        "validated": True,
                    },
                    "discovery_proof_sha256": "a" * 64,
                },
            )
        if path == "/api/v1/sandalfon/chat":
            return httpx.Response(
                200,
                json={
                    "model": "Sandalfon",
                    "version": "1.0.0",
                    "latency_ms": 5.9,
                    "hypothesis_text": "Couplage thermique",
                    "sindy": {
                        "discovered_eq_x": "dx/dt = -0.450*x + 1.500*y + 0.300*x^2"
                    },
                    "spectrum": {"precursor_hz": 11.5, "precursor_detected": True},
                    "hypothesis_test": {"validated": True},
                    "discovery_proof_sha256": "b" * 64,
                    "applied_controls": {"preset": "thermal_runaway"},
                    "spoken_reply": "Analyse Sandalfon terminée sur le couplage.",
                },
            )
        return httpx.Response(404, json={"detail": "Not found"})

    return handler


def test_default_base_url_and_api_key_headers():
    captured: list[httpx.Headers] = []
    client = Omnesight(
        api_key="omne_live_abc123",
        transport=httpx.MockTransport(_mock_handler(captured)),
    )
    assert client.base_url == "http://127.0.0.1:8001"

    res = client.hackmalim.infer(shock_amplitude=1.5, leak_node=2)
    assert isinstance(res, HackmalimInferResponse)
    assert res.model == "Hackmalim"
    assert res.stage_2_pignn["pinpointed_node"] == 2
    assert captured[0]["X-API-Key"] == "omne_live_abc123"
    assert captured[0]["Authorization"] == "Bearer omne_live_abc123"
    client.close()


def test_sandalfon_discover_and_chat():
    captured: list[httpx.Headers] = []
    client = Omnesight(
        api_key="omne_live_researcher",
        base_url="https://mlops-api.omnesight.com",
        transport=httpx.MockTransport(_mock_handler(captured)),
    )

    disc = client.sandalfon.discover(
        preset="coupled_oscillator", hypothesis_text="Test harmonic precursor"
    )
    assert isinstance(disc, SandalfonDiscoverResponse)
    assert disc.sindy["exact_support_match"] is True
    assert disc.hypothesis_test["validated"] is True

    chat = client.sandalfon.chat(
        "Teste le couplage thermique", preset="thermal_runaway"
    )
    assert isinstance(chat, SandalfonChatResponse)
    assert "Sandalfon" in chat.spoken_reply
    assert len(captured) == 2
    client.close()


def test_acl_forbidden_raises_authentication_error():
    captured: list[httpx.Headers] = []
    client = Omnesight(
        api_key="omne_live_forbidden",
        transport=httpx.MockTransport(_mock_handler(captured)),
    )
    with pytest.raises(AuthenticationError) as exc_info:
        client.hackmalim.infer()
    assert exc_info.value.status_code == 403
    client.close()


@pytest.mark.asyncio
async def test_async_client_sandalfon_discover():
    async def async_handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content.decode("utf-8"))
        assert body["preset"] == "predator_prey_grid"
        return _mock_handler([])(request)

    async with AsyncOmnesight(
        api_key="omne_live_async",
        transport=httpx.MockTransport(async_handler),
    ) as client:
        disc = await client.sandalfon.discover(preset="predator_prey_grid")
        assert disc.model == "Sandalfon"
        assert disc.spectrum["precursor_hz"] == 11.5

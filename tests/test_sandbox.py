"""
Unit tests for the Omnesight Python SDK Sandbox Environment.
Verifies offline deterministic simulation for Sandalfon, Hackmalim, Telemetry, and Reconciliation.
"""

import pytest
from omnesight import AsyncOmnesight, Omnesight


def test_sandbox_client_initialization():
    client = Omnesight(sandbox=True)
    assert client.is_sandbox is True
    assert client.api_key == "omne_sandbox_local_token"
    assert client.base_url == "https://sandbox.omnesight.com"


def test_sandbox_sandalfon_discovery():
    with Omnesight(sandbox=True) as client:
        res = client.sandalfon.discover(
            preset="thermal_runaway",
            hypothesis_text="Evaluate cable harmonic damping",
        )
        assert res.model == "sandalfon-v1.0"
        assert "discovered_eq_x" in res.sindy
        assert res.hypothesis_test["is_falsified"] is False
        assert res.spectrum["precursor_snr_db"] > 10.0


def test_sandbox_sandalfon_chat():
    with Omnesight(sandbox=True) as client:
        res = client.sandalfon.chat(message="Check telemetry harmonics")
        assert res.model == "sandalfon-v1.0"
        assert len(res.spoken_reply) > 0


def test_sandbox_hackmalim_infer():
    with Omnesight(sandbox=True) as client:
        res = client.hackmalim.infer(shock_amplitude=1.8, leak_node=3)
        assert res.model == "hackmalim-v1.0"
        assert res.stage_2_pignn["pinpointed_node"] == 3
        assert res.enterprise_guardrail["is_approved"] is True


def test_sandbox_telemetry_ingest():
    with Omnesight(sandbox=True) as client:
        res = client.telemetry.ingest(
            stream_id="stream_power_node_01",
            records=[{"device_id": "sensor_01", "metric": "temperature_c", "value": 42.5}],
        )
        assert res.records_received == 1
        assert res.records_committed == 1
        assert res.status == "COMMITTED_SANDBOX"


def test_sandbox_reconciliation_scan():
    with Omnesight(sandbox=True) as client:
        reports = client.reconciliation.scan_discrepancies(
            erp_system="AMPLITUDE", entity_type="GL_ACCOUNTS"
        )
        assert len(reports) >= 2
        assert reports[0].discrepancy_id == "DISC-SBX-001"
        assert reports[0].variance_amount_usd == 1450.00


def test_sandbox_action_protocol():
    with Omnesight(sandbox=True) as client:
        status = client.actions.get_status("ACT-SBX-001")
        assert status.action_id == "ACT-SBX-001"
        assert status.state == "SUPERVISED_APPROVAL"


@pytest.mark.asyncio
async def test_async_sandbox_client():
    async with AsyncOmnesight(sandbox=True) as aclient:
        assert aclient.is_sandbox is True
        res = await aclient.sandalfon.discover(preset="thermal_runaway")
        assert res.model == "sandalfon-v1.0"
        infer = await aclient.hackmalim.infer(shock_amplitude=1.2, leak_node=2)
        assert infer.stage_2_pignn["pinpointed_node"] == 2

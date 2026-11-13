<div align="center">

# Omnesight Python SDK

**The official Python client library for Omnesight Sovereign Operational Intelligence & Autonomous Execution Infrastructure.**

[![PyPI version](https://img.shields.io/badge/pypi-v1.1.0-blue.svg?style=flat-square)](https://pypi.org/project/omnesight/)
[![Python Versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?style=flat-square)](https://pypi.org/project/omnesight/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg?style=flat-square)](LICENSE)
[![Security Policy](https://img.shields.io/badge/security-SLA%20%3C24h-blueviolet.svg?style=flat-square)](https://github.com/Omnesight/.github/blob/main/SECURITY.md)

[Website](https://omnesight.com) • [Documentation](https://omnesight.com/docs) • [Security & Compliance](https://github.com/Omnesight/.github/blob/main/SECURITY.md) • [Support](https://github.com/Omnesight/.github/blob/main/SUPPORT.md)

</div>

---

## Overview

The **Omnesight Python SDK** provides typed access to Omnesight's sovereign Non-LLM scientific engines (**Hackmalim v1.0**, **Sandalfon v1.0**) alongside enterprise operational intelligence gateways:

* **Hackmalim v1.0 (`client.hackmalim`):** 3-layer Non-LLM control combining Continuous-Time Liquid Neural ODEs, Kirchhoff Physics-Informed GNNs, and Pearl Do-Calculus + SAT Axiom Verification.
* **Sandalfon v1.0 (`client.sandalfon`):** Sparse differential equation discovery (SINDy/STLSQ), FFT spectral wave precursor extraction, and Popperian permutation falsification.
* **Ingest Multi-Source Telemetry:** Stream telemetry from SCADA, IoT sensors, GPS fleets, and warehouse terminals in sub-second latency.
* **Closed-Loop ERP Reconciliation:** Automatically detect and resolve transactional variances across SAP S/4HANA, Oracle NetSuite, Microsoft Dynamics 365, and financial ledgers.
* **Supervised Action Protocol (SAP):** Execute automated operational interventions under deterministic governance policies and cryptographic audit trails.

---

## Installation

```bash
pip install omnesight
```

---

## Quickstart

### 1. Sovereign Scientific & Control Engines (`Hackmalim` & `Sandalfon`)

```python
from omnesight import Omnesight

# Reads OMNESIGHT_API_KEY and OMNESIGHT_BASE_URL (defaults to http://127.0.0.1:8001)
client = Omnesight(
    api_key="omne_live_your_secret_key",
    base_url="https://mlops-api.omnesight.com",
)

# Sandalfon v1.0: Extract sparse ODEs + spectral FFT wave precursors
discovery = client.sandalfon.discover(
    preset="thermal_runaway",
    noise_level=0.02,
    sparsity_threshold=0.10,
    precursor_amp=0.18,
    hypothesis_text="Cable thermal overload precursor detection",
)
print(discovery.sindy["discovered_eq_x"], discovery.hypothesis_test["z_score"])

dialogue = client.sandalfon.chat(
    message="Analyse les précurseurs thermiques sur les câbles",
    preset="thermal_runaway",
)
print(dialogue.spoken_reply)

# Hackmalim v1.0: Closed-loop Liquid ODE + PI-GNN + Causal SAT Verifier
res = client.hackmalim.infer(
    shock_amplitude=1.45,
    leak_node=2,
    leak_magnitude=22.5,
    p_max_kw=55.0,
    t_max_c=72.0,
)
print(res.target_entity_id, res.enterprise_guardrail)
```

### 2. Synchronous Enterprise Telemetry Client

```python
from omnesight import Omnesight

# Initialize the client (reads OMNESIGHT_API_KEY & OMNESIGHT_BASE_URL from environment if omitted)
client = Omnesight(
    api_key="your_api_key_here",
    base_url="https://omnesight.internal.company.com" # Your private VPC or dedicated sovereign gateway
)

# 1. Ingest asset telemetry
response = client.telemetry.ingest(
    stream_id="freight-corridor-lagos-kano",
    records=[
        {
            "device_id": "TRUCK-GPS-104",
            "metric": "cargo_seal_integrity",
            "value": 1.0,
            "metadata": {"driver": "ID-992", "cargo": "Refined Petroleum"}
        }
    ]
)
print(f"Batch {response.batch_id} ingested in {response.duration_ms}ms")

# 2. Scan ERP vs Ledger Discrepancies
discrepancies = client.reconciliation.scan_discrepancies(
    erp_system="SAP",
    entity_type="PURCHASE_ORDERS",
    lookback_days=7
)

for d in discrepancies:
    print(f"Discrepancy #{d.discrepancy_id}: Variance ${d.variance_amount_usd:,.2f} ({d.status})")
```

---

### 2. Asynchronous Client (AsyncIO / High Concurrency)

For data engineering pipelines or FastAPI backends handling thousands of events per second:

```python
import asyncio
from omnesight import AsyncOmnesight

async def main():
    async with AsyncOmnesight(api_key="your_api_key_here") as client:
        response = await client.telemetry.ingest(
            stream_id="scada-compressor-alpha",
            records=[
                {"device_id": "CMP-01", "metric": "vibration_hz", "value": 44.2}
            ]
        )
        print(f"Ingested batch: {response.batch_id}")

asyncio.run(main())
```

---

## Enterprise VPC & Sovereign Deployments

For single-tenant institutional customers running Omnesight within a private VPC (AWS, Azure, GCP, Alibaba Cloud) or air-gapped on-premise Kubernetes cluster:

```python
client = Omnesight(
    api_key="your_sovereign_vpc_token",
    base_url="https://omnesight.internal.company.com", # Private VPC endpoint
    timeout=60.0
)
```

---

## Supervised Action Protocol (SAP)

Automated write-backs to core ERPs and ledger reconciliations require policy validation:

```python
from omnesight.models import ActionApprovalRequest

# Retrieve status of an automated action staged by the cognitive engine
action = client.actions.get_status("ACT-88492")
print(f"Action: {action.action_type} | Impact: ${action.financial_impact_usd} | State: {action.state}")

# Submit human-in-the-loop supervisor approval
client.actions.submit_decision(ActionApprovalRequest(
    action_id="ACT-88492",
    action_type="ERP_LEDGER_WRITE",
    target_entity="PO-77189",
    decision="APPROVE",
    supervisor_id="SUP-MAV-01",
    supervisor_notes="Validated with physical bill of lading #BL-9921"
))
```

---

## Security & Data Sovereignty

* **Zero Frontier Model Training:** Omnesight never ingests customer transactional payloads or telemetry into public foundation model weights.
* **Cryptographic Traceability:** Every staged action is signed with a SHA-256 audit hash.
* **Security Advisories:** For vulnerability disclosure, see [SECURITY.md](https://github.com/Omnesight/.github/blob/main/SECURITY.md) or email `security@omnesight.com`.

---

## License

Apache License 2.0. See [LICENSE](LICENSE) for details.

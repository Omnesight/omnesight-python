"""
Omnesight Python SDK - Quickstart Example
Demonstrates telemetry ingestion, discrepancy scan, and supervised action verification.
"""

from omnesight import Omnesight

def main():
    # 1. Initialize client (can also read from OMNESIGHT_API_KEY environment variable)
    client = Omnesight(
        api_key="omn_live_mock_token_771829",
        base_url="https://internal.company.com" # Or your sovereign VPC: "https://omnesight.internal.company.com"
    )

    print("⚡ Omnesight Enterprise Client Initialized")

    # 2. Ingest operational telemetry from heavy assets / transport fleet
    print("\n[Step 1] Ingesting Telemetry Stream...")
    try:
        response = client.telemetry.ingest(
            stream_id="corridor-abuja-freight-08",
            records=[
                {
                    "device_id": "GPS-TRK-9901",
                    "metric": "cargo_seal_integrity",
                    "value": 1.0, # 1.0 = intact, 0.0 = compromised
                    "metadata": {"route": "Lagos-Kano", "driver_id": "DRV-442"}
                },
                {
                    "device_id": "FLOW-MTR-301",
                    "metric": "pipeline_pressure_bar",
                    "value": 68.4,
                    "unit": "bar"
                }
            ]
        )
        print(f"Batch {response.batch_id} ingested in {response.duration_ms}ms")
    except Exception as e:
        print(f"Ingestion notice (mock environment): {e}")

    # 3. Trigger ERP vs Operational Ledger Discrepancy Scan
    print("\n[Step 2] Scanning ERP Purchase Orders vs Delivery Receipts...")
    try:
        discrepancies = client.reconciliation.scan_discrepancies(
            erp_system="SAP",
            entity_type="PURCHASE_ORDERS",
            lookback_days=14
        )
        print(f"Found {len(discrepancies)} operational discrepancies.")
        for disc in discrepancies:
            print(f"- Discrepancy #{disc.discrepancy_id}: Variance ${disc.variance_amount_usd:,.2f} ({disc.status})")
    except Exception as e:
        print(f"Reconciliation notice (mock environment): {e}")

    print("\n✅ Quickstart completed successfully.")

if __name__ == "__main__":
    main()

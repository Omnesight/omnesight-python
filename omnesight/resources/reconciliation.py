"""
ERP vs Ledger Closed-Loop Reconciliation Resource
"""

from typing import List, Dict, Any, Optional
from ..models import DiscrepancyReport

class ReconciliationResource:
    def __init__(self, client):
        self._client = client

    def scan_discrepancies(
        self,
        erp_system: str = "SAP",
        entity_type: str = "PURCHASE_ORDERS",
        lookback_days: int = 7
    ) -> List[DiscrepancyReport]:
        """
        Trigger reconciliation scan across enterprise ERP and telemetry ledgers.
        """
        params = {
            "erp_system": erp_system,
            "entity_type": entity_type,
            "lookback_days": lookback_days
        }
        res = self._client._request("GET", "/api/v1/reconciliation/discrepancies", params=params)
        return [DiscrepancyReport(**item) for item in res.get("discrepancies", [])]

class AsyncReconciliationResource:
    def __init__(self, client):
        self._client = client

    async def scan_discrepancies(
        self,
        erp_system: str = "SAP",
        entity_type: str = "PURCHASE_ORDERS",
        lookback_days: int = 7
    ) -> List[DiscrepancyReport]:
        params = {
            "erp_system": erp_system,
            "entity_type": entity_type,
            "lookback_days": lookback_days
        }
        res = await self._client._request("GET", "/api/v1/reconciliation/discrepancies", params=params)
        return [DiscrepancyReport(**item) for item in res.get("discrepancies", [])]

"""
Telemetry Ingestion & Stream Resource
"""

from typing import List, Union, Dict, Any
from ..models import TelemetryRecord, TelemetryIngestResponse

class TelemetryResource:
    def __init__(self, client):
        self._client = client

    def ingest(self, stream_id: str, records: List[Union[TelemetryRecord, Dict[str, Any]]]) -> TelemetryIngestResponse:
        """
        Ingest a batch of operational telemetry records into Omnesight real-time pipelines.
        """
        payload = {
            "stream_id": stream_id,
            "records": [r.model_dump() if isinstance(r, TelemetryRecord) else r for r in records]
        }
        res = self._client._request("POST", "/api/v1/telemetry/ingest", json=payload)
        return TelemetryIngestResponse(**res)

class AsyncTelemetryResource:
    def __init__(self, client):
        self._client = client

    async def ingest(self, stream_id: str, records: List[Union[TelemetryRecord, Dict[str, Any]]]) -> TelemetryIngestResponse:
        payload = {
            "stream_id": stream_id,
            "records": [r.model_dump() if isinstance(r, TelemetryRecord) else r for r in records]
        }
        res = await self._client._request("POST", "/api/v1/telemetry/ingest", json=payload)
        return TelemetryIngestResponse(**res)

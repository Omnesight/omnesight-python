"""
Omnesight SDK Models & Schemas (Pydantic v2)
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class TelemetryRecord(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    device_id: str
    metric: str
    value: float
    unit: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

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
    recommended_action_id: Optional[str] = None

class ActionApprovalRequest(BaseModel):
    action_id: str
    action_type: str
    target_entity: str
    decision: str # "APPROVE" | "REJECT" | "MODIFIED"
    supervisor_id: str
    supervisor_notes: Optional[str] = None

class ActionStatusResponse(BaseModel):
    action_id: str
    state: str # "PROPOSED", "SUPERVISED_APPROVAL", "COMMITTED", "REVERTED"
    action_type: str
    financial_impact_usd: float
    sha256_audit_hash: str
    executed_at: Optional[datetime] = None

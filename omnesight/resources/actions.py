"""
Supervised Action Protocol (SAP) Resource
Governs automated policy execution with cryptographic provenance.
"""

from typing import Dict, Any, Optional
from ..models import ActionApprovalRequest, ActionStatusResponse

class ActionsResource:
    def __init__(self, client):
        self._client = client

    def get_status(self, action_id: str) -> ActionStatusResponse:
        """
        Retrieve state, cryptographic SHA-256 hash, and execution log of an action.
        """
        res = self._client._request("GET", f"/api/v1/actions/{action_id}")
        return ActionStatusResponse(**res)

    def submit_decision(self, approval: ActionApprovalRequest) -> ActionStatusResponse:
        """
        Submit a human supervisor decision (APPROVE, REJECT, MODIFIED) for a staged action.
        """
        res = self._client._request("POST", f"/api/v1/actions/{approval.action_id}/decision", json=approval.model_dump())
        return ActionStatusResponse(**res)

class AsyncActionsResource:
    def __init__(self, client):
        self._client = client

    async def get_status(self, action_id: str) -> ActionStatusResponse:
        res = await self._client._request("GET", f"/api/v1/actions/{action_id}")
        return ActionStatusResponse(**res)

    async def submit_decision(self, approval: ActionApprovalRequest) -> ActionStatusResponse:
        res = await self._client._request("POST", f"/api/v1/actions/{approval.action_id}/decision", json=approval.model_dump())
        return ActionStatusResponse(**res)

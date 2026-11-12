"""
Withdrawal API — OPS05, SEC05.
Serialized immediate withdrawal: blocks retrieval instantly, cache cleanup ≤ 5 minutes.
"""
from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.importer.withdrawal import ImmediateWithdrawalService

router = APIRouter()


class WithdrawalRequest(BaseModel):
    entity_type: Literal["passage", "critical_field", "crm_record"]
    entity_id: str
    actor_role: str
    reason: str


class WithdrawalResponse(BaseModel):
    tombstone_id: str
    entity_type: str
    entity_id: str
    withdrawn_at: str
    acknowledged: bool


@router.post(
    "/",
    response_model=WithdrawalResponse,
    status_code=200,
    summary="Immediate policy withdrawal (OPS05, SEC05)",
)
async def execute_withdrawal(request: WithdrawalRequest):
    """
    Immediately withdraws a passage, critical field, or CRM record.
    Implementation requirements:
    - Serialized at DB level (not application level) to prevent race conditions (SEC05).
    - After acknowledgment: no affected response may be newly served or reused.
    - Cache cleanup target: ≤ 5 minutes (SEC05).
    - Separate from batch cycle — acts immediately without awaiting next batch.
    """
    service = ImmediateWithdrawalService()
    try:
        if request.entity_type == "passage":
            res = service.withdraw_policy_passage(
                passage_id=request.entity_id,
                role=request.actor_role,
                reason=request.reason,
            )
        elif request.entity_type == "critical_field":
            res = service.withdraw_critical_rule(
                rule_id=request.entity_id,
                role=request.actor_role,
                reason=request.reason,
            )
        elif request.entity_type == "crm_record":
            res = service.withdraw_crm_record(
                record_key=request.entity_id,
                role=request.actor_role,
                reason=request.reason,
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported entity_type '{request.entity_type}'")

        return WithdrawalResponse(
            tombstone_id=res["withdrawal_id"],
            entity_type=res["entity_type"],
            entity_id=res["entity_id"],
            withdrawn_at=res["withdrawn_at"],
            acknowledged=True,
        )
    except ValueError as val_err:
        raise HTTPException(status_code=404, detail=str(val_err))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

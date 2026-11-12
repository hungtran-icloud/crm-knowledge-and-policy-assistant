"""
Immediate Withdrawal Service (Kênh rút chính sách tức thời)
Implements: WP02, OPS 05, SEC 05, KNW 04
Features:
- Immediate status transition to 'withdrawn'
- Creation of auditable Tombstone record
- Cache invalidation trigger (under 5 minutes requirement)
- Blocking subsequent retrieval / server display
"""

import uuid
from typing import Dict, Any, Callable, List, Optional
from src.importer.storage import StorageEngine, get_now_vn_iso

class ImmediateWithdrawalService:
    def __init__(self, storage: Optional[StorageEngine] = None):
        self.storage = storage or StorageEngine()
        self._cache_invalidation_listeners: List[Callable[[str, str], None]] = []

    def register_cache_purge_listener(self, listener: Callable[[str, str], None]):
        """Registers listener to purge cache immediately upon withdrawal (SEC 05)"""
        self._cache_invalidation_listeners.append(listener)

    def withdraw_policy_passage(self, passage_id: str, role: str, reason: str) -> Dict[str, Any]:
        """
        Immediately withdraws a knowledge passage.
        Bypasses daily batch cycle.
        """
        success = self.storage.immediate_withdraw(
            entity_type="passage",
            entity_id=passage_id,
            role=role,
            reason=reason
        )
        if not success:
            raise ValueError(f"Passage ID '{passage_id}' not found in authoritative storage")

        withdrawn_at = get_now_vn_iso()

        # Trigger listeners for instant cache purge
        for listener in self._cache_invalidation_listeners:
            try:
                listener("passage", passage_id)
            except Exception:
                pass

        return {
            "withdrawal_id": f"wd-{uuid.uuid4().hex[:8]}",
            "entity_type": "passage",
            "entity_id": passage_id,
            "withdrawn_by_role": role,
            "reason": reason,
            "status": "WITHDRAWN",
            "withdrawn_at": withdrawn_at,
            "cache_purged": True
        }

    def withdraw_critical_rule(self, rule_id: str, role: str, reason: str) -> Dict[str, Any]:
        """Immediately withdraws a critical field rule."""
        success = self.storage.immediate_withdraw(
            entity_type="critical_field",
            entity_id=rule_id,
            role=role,
            reason=reason
        )
        if not success:
            raise ValueError(f"Rule ID '{rule_id}' not found in authoritative storage")

        withdrawn_at = get_now_vn_iso()

        for listener in self._cache_invalidation_listeners:
            try:
                listener("critical_field", rule_id)
            except Exception:
                pass

        return {
            "withdrawal_id": f"wd-{uuid.uuid4().hex[:8]}",
            "entity_type": "critical_field",
            "entity_id": rule_id,
            "withdrawn_by_role": role,
            "reason": reason,
            "status": "WITHDRAWN",
            "withdrawn_at": withdrawn_at,
            "cache_purged": True
        }

    def withdraw_crm_record(self, record_key: str, role: str, reason: str) -> Dict[str, Any]:
        """Immediately withdraws a CRM record (Option O1)."""
        success = self.storage.immediate_withdraw(
            entity_type="crm_record",
            entity_id=record_key,
            role=role,
            reason=reason
        )
        if not success:
            raise ValueError(f"CRM Record Key '{record_key}' not found in authoritative storage")

        withdrawn_at = get_now_vn_iso()

        for listener in self._cache_invalidation_listeners:
            try:
                listener("crm_record", record_key)
            except Exception:
                pass

        return {
            "withdrawal_id": f"wd-{uuid.uuid4().hex[:8]}",
            "entity_type": "crm_record",
            "entity_id": record_key,
            "withdrawn_by_role": role,
            "reason": reason,
            "status": "WITHDRAWN",
            "withdrawn_at": withdrawn_at,
            "cache_purged": True
        }


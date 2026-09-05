from datetime import datetime, timedelta
from typing import Any
from app.services.context.base import SharedWorkflowContext
from app.services.rules.base import DeterministicRule

class DormancyDetectionRule(DeterministicRule):
    def __init__(self):
        super().__init__(
            rule_id="R-ATT-001",
            name="Dormancy Detection",
            reason_code="ENGAGEMENT_LOW",
            description="Triggered if member has 0 attendance records in recent summary."
        )

    def evaluate(self, context: SharedWorkflowContext) -> tuple[bool, int, dict[str, Any]]:
        # Deterministic logic: no check-ins in the last 30 days = triggered.
        records = context.attendance_summary.get("records", [])
        cutoff = datetime.utcnow() - timedelta(days=30)
        recent_records = []
        for record in records:
            raw_checked_in_at = record.get("checked_in_at")
            if not raw_checked_in_at:
                continue
            try:
                checked_in_at = datetime.fromisoformat(raw_checked_in_at)
            except ValueError:
                continue
            if checked_in_at >= cutoff:
                recent_records.append(record)

        if not recent_records:
            return True, 50, {"reason": "No attendance in the last 30 days"}
        return False, 0, {}

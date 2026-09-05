from typing import Any
from app.services.context.base import SharedWorkflowContext
from app.services.rules.base import DeterministicRule

class FollowUpRequiredRule(DeterministicRule):
    def __init__(self):
        super().__init__(
            rule_id="R-FOL-001",
            name="Follow-up Required",
            reason_code="FOLLOWUP_PENDING",
            description="Triggered if member has no recent follow-ups."
        )

    def evaluate(self, context: SharedWorkflowContext) -> tuple[bool, int, dict[str, Any]]:
        if not context.follow_up_summary.get("activities"):
            return True, 30, {"reason": "No recent follow-up"}
        return False, 0, {}

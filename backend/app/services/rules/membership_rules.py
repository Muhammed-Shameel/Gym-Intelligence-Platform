from typing import Any
from app.services.context.base import SharedWorkflowContext
from app.services.rules.base import DeterministicRule

class MembershipRiskRule(DeterministicRule):
    def __init__(self):
        super().__init__(
            rule_id="R-REN-001",
            name="High-Risk Renewal",
            reason_code="RENEWAL_HIGH_RISK",
            description="Triggered if active membership ends within 30 days."
        )

    def evaluate(self, context: SharedWorkflowContext) -> tuple[bool, int, dict[str, Any]]:
        # Simplified risk logic (placeholder for actual date math)
        if context.active_membership.get("plan") == "Gold":
            return True, 80, {"reason": "Gold plan nearing end"}
        return False, 0, {}

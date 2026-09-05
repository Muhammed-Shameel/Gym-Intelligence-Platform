from typing import Any
from app.services.context.base import SharedWorkflowContext
from app.services.rules.base import DeterministicRule

class TrainerCapacityRule(DeterministicRule):
    def __init__(self):
        super().__init__(
            rule_id="R-TRA-001",
            name="Trainer Capacity",
            reason_code="TRAINER_AT_CAPACITY",
            description="Triggered if trainer assigned is at capacity."
        )

    def evaluate(self, context: SharedWorkflowContext) -> tuple[bool, int, dict[str, Any]]:
        # Deterministic logic: placeholder check
        if not context.trainer_assignment:
            return True, 40, {"reason": "No trainer assigned"}
        return False, 0, {}

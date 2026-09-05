from dataclasses import dataclass
from typing import Any
from app.services.context.base import SharedWorkflowContext

@dataclass(frozen=True)
class DeterministicRule:
    rule_id: str
    name: str
    reason_code: str
    description: str

    def evaluate(self, context: SharedWorkflowContext) -> tuple[bool, int, dict[str, Any]]:
        """Evaluate rule against the context. Returns (triggered, score, metadata)."""
        raise NotImplementedError("Implement concrete rules in subclasses")

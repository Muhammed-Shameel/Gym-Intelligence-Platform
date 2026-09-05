from typing import Any
from app.services.context.base import SharedWorkflowContext
from app.services.agents.base import DeterministicAgent
from app.services.rules.engine import RuleEngine
from app.services.rules.membership_rules import MembershipRiskRule

class EngagementRiskAgent(DeterministicAgent):
    def __init__(self):
        super().__init__(name="EngagementRiskAgent")
        self.rules = [MembershipRiskRule()]
        self.engine = RuleEngine()

    def run(self, context: SharedWorkflowContext) -> dict[str, Any]:
        result = self.engine.evaluate_rules(context, self.rules)
        return {
            "agent": self.name,
            "assessment": result,
            "recommendation": "Review high-value membership" if result["aggregate_score"] > 50 else "Standard monitoring"
        }

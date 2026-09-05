from typing import Any
from app.services.context.base import SharedWorkflowContext
from app.services.agents.base import DeterministicAgent
from app.services.rules.engine import RuleEngine
from app.services.rules.followup_rules import FollowUpRequiredRule

class FollowUpRecommendationAgent(DeterministicAgent):
    def __init__(self):
        super().__init__(name="FollowUpRecommendationAgent")
        self.rules = [FollowUpRequiredRule()]
        self.engine = RuleEngine()

    def run(self, context: SharedWorkflowContext) -> dict[str, Any]:
        result = self.engine.evaluate_rules(context, self.rules)
        return {
            "agent": self.name,
            "assessment": result,
            "recommendation": "Schedule outreach" if result["aggregate_score"] > 0 else "Outreach up-to-date"
        }

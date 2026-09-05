from typing import Any
from app.services.context.base import SharedWorkflowContext
from app.services.agents.base import DeterministicAgent
from app.services.rules.engine import RuleEngine
from app.services.rules.trainer_rules import TrainerCapacityRule

class TrainerAllocationAgent(DeterministicAgent):
    def __init__(self):
        super().__init__(name="TrainerAllocationAgent")
        self.rules = [TrainerCapacityRule()]
        self.engine = RuleEngine()

    def run(self, context: SharedWorkflowContext) -> dict[str, Any]:
        result = self.engine.evaluate_rules(context, self.rules)
        return {
            "agent": self.name,
            "assessment": result,
            "recommendation": "Assign new trainer" if result["aggregate_score"] > 0 else "Trainer allocation stable"
        }

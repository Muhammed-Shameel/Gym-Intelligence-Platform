from typing import Any
from app.services.context.base import SharedWorkflowContext
from app.services.agents.base import DeterministicAgent
from app.services.rules.engine import RuleEngine
from app.services.rules.attendance_rules import DormancyDetectionRule

class AttendanceAgent(DeterministicAgent):
    def __init__(self):
        super().__init__(name="AttendanceAgent")
        self.rules = [DormancyDetectionRule()]
        self.engine = RuleEngine()

    def run(self, context: SharedWorkflowContext) -> dict[str, Any]:
        """Evaluates engagement and returns deterministic assessment."""
        result = self.engine.evaluate_rules(context, self.rules)
        
        # Determine actionable recommendation
        recommendation = "Maintain current engagement"
        if result["aggregate_score"] >= 50:
            recommendation = "Trigger reactivation outreach"
            
        return {
            "agent": self.name,
            "assessment": result,
            "recommendation": recommendation
        }

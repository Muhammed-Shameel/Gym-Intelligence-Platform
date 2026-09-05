from typing import Any
from app.services.context.base import SharedWorkflowContext
from app.services.rules.base import DeterministicRule

class RuleEngine:
    def evaluate_rules(self, context: SharedWorkflowContext, rules: list[DeterministicRule]) -> dict[str, Any]:
        """Orchestrates rule evaluation, aggregating triggered rules."""
        triggered_rules = []
        total_score = 0
        
        for rule in rules:
            triggered, score, metadata = rule.evaluate(context)
            if triggered:
                triggered_rules.append({
                    "rule_id": rule.rule_id,
                    "reason_code": rule.reason_code,
                    "metadata": metadata
                })
                total_score += score
                
        return {
            "triggered_rules": triggered_rules,
            "aggregate_score": total_score
        }

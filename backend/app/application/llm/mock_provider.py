import json
from typing import Dict, Any

class MockLLMProvider:
    """
    Mock LLM Provider for Stage 4 LLM Agent Integration.
    Generates predictable, valid structured JSON output matching schema without requiring external API keys.
    """
    def __init__(self, model_name: str = "mock-agentic-v1"):
        self.model_name = model_name

    def generate(self, prompt: str, safe_context: Dict[str, Any], recommendation: str) -> str:
        route = safe_context.get("selected_route", "standard")
        attendance = safe_context.get("attendance_metrics", {})
        risk = safe_context.get("engagement_risk", {})
        trainer = safe_context.get("trainer_assignment", {})

        checkins = attendance.get("checkins_last_30_days", 0)
        days_since = attendance.get("days_since_last_checkin", 0)
        risk_level = risk.get("risk_level", "low")
        has_active_trainer = trainer.get("has_active_trainer", True)

        trainer_note = ""
        trainer_observation = None
        if "Assign new trainer" in recommendation or not has_active_trainer:
            trainer_note = " A trainer assignment is missing, so staff should assign a new trainer separately from attendance follow-up."
            trainer_observation = "No active trainer assignment is available."

        if checkins == 0 or route == "dormant" or attendance.get("is_dormant"):
            summary_text = (
                f"[MOCK LLM] Member has been inactive for {days_since} days with only {checkins} check-in(s) in the last month. "
                f"Recent attendance is low and should be reviewed before assuming healthy engagement.{trainer_note}"
            )
            obs = [
                "No check-ins recorded in the last 30 days.",
                "Attendance evidence does not support a regular-visits interpretation."
            ]
            risks = ["Member churn risk", "Loss of routine habits"]
        elif route == "high_risk" or risk_level == "high":
            summary_text = (
                f"[MOCK LLM] Member displays elevated churn risk indicators (risk score {risk.get('risk_score', 0.8)}). "
                f"Urgent personalized check-in and workout plan adjustment recommended.{trainer_note}"
            )
            obs = [
                "Attendance frequency declining significantly.",
                "Engagement risk flag triggered."
            ]
            risks = ["Imminent membership drop", "Decreased facility utilization"]
        else:
            summary_text = (
                f"[MOCK LLM] Member maintains regular facility visits ({checkins} in last 30 days). "
                f"Standard workout progression and trainer guidance recommended.{trainer_note}"
            )
            obs = [
                "Consistent workout schedule maintained.",
                "Positive engagement indicators."
            ]
            risks = []

        if trainer_observation:
            obs.append(trainer_observation)

        output = {
            "agent_name": "ExplanationSummaryService",
            "mode": "llm_assisted",
            "summary": summary_text,
            "observations": obs,
            "recommendation": recommendation,
            "confidence": 0.95 if checkins > 0 or "Maintain current engagement" not in recommendation else 0.72,
            "risks": risks,
            "missing_information": [],
            "protected_fields_changed": False,
            "should_fallback": False
        }
        return json.dumps(output)

from typing import Any
from pydantic import BaseModel, Field

class AgentOutput(BaseModel):
    agent_name: str
    workflow_session_id: str
    member_id: str
    status: str = "completed"
    classification: str | None = None
    score: int | None = Field(default=None, ge=0, le=100)
    recommendation: str | None = None
    reasons: list[str] = []
    rules_triggered: list[str] = []
    evidence: dict[str, Any] = {}
    context_updated: list[str] = []

class RuleResult(BaseModel):
    rule_id: str
    triggered: bool
    reason_code: str
    points: int = 0
    evidence: dict[str, Any] = {}

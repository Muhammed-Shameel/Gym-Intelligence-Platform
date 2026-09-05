from typing import Any
from pydantic import BaseModel, Field, ValidationError, model_validator

class SharedWorkflowContext(BaseModel):
    workflow_session_id: str
    member_id: str
    review_reason: str = "general_review"
    member_profile: dict[str, Any] = Field(default_factory=dict)
    active_membership: dict[str, Any] = Field(default_factory=dict)
    attendance_summary: dict[str, Any] = Field(default_factory=dict)
    trainer_assignment: dict[str, Any] = Field(default_factory=dict)
    trainer_candidates: list[dict[str, Any]] = Field(default_factory=list)
    follow_up_summary: dict[str, Any] = Field(default_factory=dict)
    agent_outputs: dict[str, Any] = Field(default_factory=dict)
    final_decision: dict[str, Any] = Field(default_factory=dict)
    explanation: str = ""
    audit_status: str = "pending"
    audit_reference: str | None = None

    @classmethod
    def create_scoped_context(cls, session_id: str, member_id: str, **kwargs) -> "SharedWorkflowContext":
        """Factory method to initialize run-scoped context."""
        return cls(workflow_session_id=session_id, member_id=member_id, **kwargs)

    @model_validator(mode='after')
    def validate_completeness(self) -> "SharedWorkflowContext":
        """Ensure critical fields are populated after initialization."""
        if not self.workflow_session_id or not self.member_id:
            raise ValueError("workflow_session_id and member_id are required.")
        return self

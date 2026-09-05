import pytest
from pydantic import ValidationError
from app.services.context.base import SharedWorkflowContext

def test_context_initialization():
    ctx = SharedWorkflowContext.create_scoped_context(
        session_id="test-session",
        member_id="m123"
    )
    assert ctx.workflow_session_id == "test-session"
    assert ctx.member_id == "m123"
    assert ctx.audit_status == "pending"

def test_context_validation_failure():
    with pytest.raises(ValidationError):
        # Trigger validation failure (missing critical fields)
        SharedWorkflowContext(workflow_session_id="", member_id="")

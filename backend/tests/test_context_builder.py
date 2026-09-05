import pytest
from app.models.domain import Member, Membership
from app.services.context.builder import ContextBuilder
from datetime import date

def test_build_context_success(db):
    # Setup test data
    member = Member(member_code="m1", full_name="John Doe", joined_on=date(2023, 1, 1))
    db.add(member)
    db.commit()
    db.refresh(member)
    
    membership = Membership(member_id=member.id, plan_name="Gold", start_date=date(2023, 1, 1), end_date=date(2024, 1, 1))
    db.add(membership)
    db.commit()
    
    # Run test
    builder = ContextBuilder(db)
    ctx = builder.build_context(session_id="s1", member_id=member.id)
    
    assert ctx.workflow_session_id == "s1"
    assert ctx.member_id == member.id
    assert ctx.member_profile["full_name"] == "John Doe"
    assert ctx.active_membership["plan"] == "Gold"

def test_build_context_member_not_found(db):
    builder = ContextBuilder(db)
    with pytest.raises(ValueError, match="Member with ID non-existent not found."):
        builder.build_context(session_id="s1", member_id="non-existent")

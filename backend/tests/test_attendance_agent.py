from app.services.context.base import SharedWorkflowContext
from app.services.agents.attendance_agent import AttendanceAgent

def test_attendance_agent_dormant():
    # Setup dormant context
    ctx = SharedWorkflowContext.create_scoped_context(session_id="s1", member_id="m1")
    ctx.attendance_summary = {"records": []} # Empty list
    
    agent = AttendanceAgent()
    result = agent.run(ctx)
    
    assert result["recommendation"] == "Trigger reactivation outreach"
    assert len(result["assessment"]["triggered_rules"]) == 1
    assert result["assessment"]["triggered_rules"][0]["rule_id"] == "R-ATT-001"

def test_attendance_agent_active():
    # Setup active context
    ctx = SharedWorkflowContext.create_scoped_context(session_id="s1", member_id="m1")
    ctx.attendance_summary = {"records": [{"checked_in_at": "2026-08-20"}]}
    
    agent = AttendanceAgent()
    result = agent.run(ctx)
    
    assert result["recommendation"] == "Maintain current engagement"
    assert len(result["assessment"]["triggered_rules"]) == 0

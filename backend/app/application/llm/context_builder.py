from datetime import datetime, timedelta
from typing import Dict, Any

class SafeContextBuilder:
    """
    Safe Context Builder for LLM Node.
    Extracts minimal, sanitized summary context from LangGraph state / SharedWorkflowContext.
    Enforces boundary: No full DB dumps, no secret credentials.
    """
    @staticmethod
    def build_safe_context(state: Dict[str, Any]) -> Dict[str, Any]:
        shared_ctx = state.get("shared_context", {})
        
        # Extract member profile summary (sanitized)
        member_profile = shared_ctx.get("member_profile", {})
        safe_member = {
            "member_id": member_profile.get("member_id", state.get("member_id", "unknown")),
            "membership_tier": member_profile.get("membership_tier", "standard"),
            "primary_goal": member_profile.get("primary_goal", "general_fitness")
        }
        
        # Extract attendance metrics from either precomputed metrics or raw records.
        attendance = shared_ctx.get("attendance_metrics", {})
        attendance_records = shared_ctx.get("attendance_summary", {}).get("records", [])
        recent_cutoff = datetime.utcnow() - timedelta(days=30)
        recent_checkins = 0
        days_since_last_checkin = attendance.get("days_since_last_checkin")

        parsed_checkins = []
        for record in attendance_records:
            raw_checked_in_at = record.get("checked_in_at")
            if not raw_checked_in_at:
                continue
            try:
                checked_in_at = datetime.fromisoformat(raw_checked_in_at)
            except ValueError:
                continue
            parsed_checkins.append(checked_in_at)
            if checked_in_at >= recent_cutoff:
                recent_checkins += 1

        if days_since_last_checkin is None and parsed_checkins:
            latest_checkin = max(parsed_checkins)
            days_since_last_checkin = max((datetime.utcnow() - latest_checkin).days, 0)
        elif days_since_last_checkin is None:
            days_since_last_checkin = 999

        checkins_last_30_days = attendance.get("checkins_last_30_days", recent_checkins)
        safe_attendance = {
            "checkins_last_30_days": checkins_last_30_days,
            "days_since_last_checkin": days_since_last_checkin,
            "is_dormant": attendance.get("is_dormant", checkins_last_30_days == 0)
        }

        trainer_assignment = shared_ctx.get("trainer_assignment", {})
        safe_trainer = {
            "has_active_trainer": bool(trainer_assignment),
            "trainer_id": trainer_assignment.get("trainer_id")
        }
        
        # Extract engagement risk
        engagement = shared_ctx.get("engagement_risk", {})
        safe_engagement = {
            "risk_score": engagement.get("risk_score", 0.0),
            "risk_level": engagement.get("risk_level", "low")
        }
        
        # Extract agent outputs summary
        agent_outputs_summary = []
        for item in state.get("agent_outputs", []):
            agent_outputs_summary.append({
                "agent": item.get("agent"),
                "recommendation": item.get("output", {}).get("recommendation", "")
            })
            
        return {
            "workflow_id": state.get("workflow_id", "unknown"),
            "member_profile": safe_member,
            "attendance_metrics": safe_attendance,
            "trainer_assignment": safe_trainer,
            "engagement_risk": safe_engagement,
            "selected_route": state.get("selected_route", "standard"),
            "route_reason": state.get("route_reason", ""),
            "agent_outputs_summary": agent_outputs_summary,
            "final_recommendation": state.get("final_recommendation", "")
        }

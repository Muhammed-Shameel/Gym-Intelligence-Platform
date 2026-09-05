from typing import Any
from app.services.context.base import SharedWorkflowContext
from app.services.agents.attendance_agent import AttendanceAgent
from app.services.agents.engagement_agent import EngagementRiskAgent
from app.services.agents.trainer_agent import TrainerAllocationAgent
from app.services.agents.followup_agent import FollowUpRecommendationAgent
from datetime import datetime

class OrchestrationService:
    def __init__(self):
        # Approved deterministic sequence
        self.agents = [
            AttendanceAgent(),
            EngagementRiskAgent(),
            TrainerAllocationAgent(),
            FollowUpRecommendationAgent()
        ]

    def run_workflow(self, context: SharedWorkflowContext) -> dict[str, Any]:
        """Runs agents in a deterministic sequence and aggregates results."""
        results = {}
        logs = []
        
        for agent in self._select_agents(context):
            start_time = datetime.utcnow()
            agent_result = agent.run(context)
            end_time = datetime.utcnow()
            
            # Log execution
            logs.append({
                "agent": agent.name,
                "input": context.model_dump(),
                "output": agent_result,
                "started_at": str(start_time),
                "completed_at": str(end_time)
            })
            results[agent.name] = agent_result
        
        # Aggregate recommendation
        final_rec = self._aggregate_recommendations(results)
        
        # Populate explanation
        context.explanation = f"Workflow completed with recommendation: {final_rec}. Based on agents: {', '.join(results.keys())}."
        
        return {
            "workflow_session_id": context.workflow_session_id,
            "results": results,
            "final_recommendation": final_rec,
            "trace_log": logs,
            "context": context.model_dump()
        }

    def _select_agents(self, context: SharedWorkflowContext):
        """Apply the same routing intent as the LangGraph workflow."""
        attendance_agent = self.agents[0]
        attendance_result = attendance_agent.run(context)

        if attendance_result["assessment"]["aggregate_score"] >= 50:
            return [self.agents[0], self.agents[3]]

        engagement_agent = self.agents[1]
        engagement_result = engagement_agent.run(context)
        if engagement_result["assessment"]["aggregate_score"] > 50:
            return [self.agents[0], self.agents[1], self.agents[3]]

        return self.agents

    def _aggregate_recommendations(self, results: dict[str, Any]) -> str:
        """Deterministic aggregation rule."""
        recs = [res["recommendation"] for res in results.values()]
        return " | ".join(recs)

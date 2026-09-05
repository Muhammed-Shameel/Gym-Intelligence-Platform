from langgraph.graph import StateGraph, END
from app.services.orchestrators.state import GFIPGraphState
from app.services.agents.attendance_agent import AttendanceAgent
from app.services.agents.engagement_agent import EngagementRiskAgent
from app.services.agents.trainer_agent import TrainerAllocationAgent
from app.services.agents.followup_agent import FollowUpRecommendationAgent
from app.services.agents.summary_agent import SummaryAgent
from datetime import datetime

# Initialize agents
attendance_agent = AttendanceAgent()
engagement_agent = EngagementRiskAgent()
trainer_agent = TrainerAllocationAgent()
followup_agent = FollowUpRecommendationAgent()
summary_agent = SummaryAgent()

from app.services.context.base import SharedWorkflowContext

# Node Wrappers
def attendance_node(state: GFIPGraphState) -> GFIPGraphState:
    state["executed_path"].append("attendance")
    ctx = SharedWorkflowContext(**state["shared_context"]) 
    result = attendance_agent.run(ctx)
    state["agent_outputs"].append({"agent": "AttendanceAgent", "output": result})
    # Update flags based on attendance
    state["route_flags"] = {
        **state["route_flags"],
        "is_dormant": result.get("assessment", {}).get("aggregate_score", 0) >= 50,
    }
    return state

def engagement_risk_node(state: GFIPGraphState) -> GFIPGraphState:
    state["executed_path"].append("engagement")
    ctx = SharedWorkflowContext(**state["shared_context"])
    result = engagement_agent.run(ctx)
    state["agent_outputs"].append({"agent": "EngagementRiskAgent", "output": result})
    state["route_flags"] = {
        **state["route_flags"],
        "is_high_risk": result.get("assessment", {}).get("aggregate_score", 0) > 50,
    }
    return state

def trainer_allocation_node(state: GFIPGraphState) -> GFIPGraphState:
    state["executed_path"].append("trainer")
    ctx = SharedWorkflowContext(**state["shared_context"])
    result = trainer_agent.run(ctx)
    state["agent_outputs"].append({"agent": "TrainerAllocationAgent", "output": result})
    return state

def followup_recommendation_node(state: GFIPGraphState) -> GFIPGraphState:
    state["executed_path"].append("followup")
    ctx = SharedWorkflowContext(**state["shared_context"])
    result = followup_agent.run(ctx)
    state["agent_outputs"].append({"agent": "FollowUpRecommendationAgent", "output": result})
    return state

def router_node(state: GFIPGraphState) -> GFIPGraphState:
    state["executed_path"].append("router")
    if state["route_flags"].get("is_dormant"):
        state["selected_route"] = "dormant"
        state["route_reason"] = "Member is dormant; skipping engagement and trainer allocation."
        state["skipped_agents"].extend([
            {"agent": "EngagementRiskAgent", "reason": "Dormant route"},
            {"agent": "TrainerAllocationAgent", "reason": "Dormant route"}
        ])
    elif state["route_flags"].get("is_high_risk"):
        state["selected_route"] = "high_risk"
        state["route_reason"] = "Member is high risk; skipping trainer allocation for urgent intervention."
        state["skipped_agents"].append({"agent": "TrainerAllocationAgent", "reason": "High-risk route"})
    else:
        state["selected_route"] = "standard"
        state["route_reason"] = "Standard processing."
    return state

def recommendation_node(state: GFIPGraphState) -> GFIPGraphState:
    state["executed_path"].append("recommendation")
    recs = [res["output"]["recommendation"] for res in state["agent_outputs"]]
    state["final_recommendation"] = " | ".join(recs)
    return state

from app.application.llm.llm_service import LLMService

llm_service = LLMService()

def summary_node(state: GFIPGraphState) -> GFIPGraphState:
    state["executed_path"].append("summary")
    ctx = SharedWorkflowContext(**state["shared_context"])
    result = summary_agent.run(ctx, state["final_recommendation"])
    state["agent_outputs"].append({"agent": "ExplanationSummaryService", "output": result})
    state["explanation"] = result["summary"]
    state["llm_mode"] = "disabled"
    state["llm_provider"] = "none"
    state["llm_model"] = "none"
    state["llm_validation_status"] = "skipped"
    state["fallback_used"] = True
    state["fallback_reason"] = "Standard LangGraph mode (LLM disabled)"
    state["protected_fields_changed"] = False
    return state

def summary_llm_node(state: GFIPGraphState) -> GFIPGraphState:
    state["executed_path"].append("summary_llm")
    output_dict, audit_meta = llm_service.execute_summary_node(state, state["final_recommendation"])
    
    state["agent_outputs"].append({"agent": "ExplanationSummaryService", "output": output_dict})
    state["explanation"] = output_dict.get("summary", "")
    
    # Store audit metadata in graph state
    state["llm_mode"] = "llm_assisted" if not audit_meta.get("fallback_used") else "fallback"
    state["llm_provider"] = audit_meta.get("provider", "mock")
    state["llm_model"] = audit_meta.get("model", "mock-agentic-v1")
    state["llm_validation_status"] = audit_meta.get("validation_status", "passed")
    state["fallback_used"] = audit_meta.get("fallback_used", False)
    state["fallback_reason"] = audit_meta.get("fallback_reason")
    state["llm_metadata"] = audit_meta
    state["protected_fields_changed"] = audit_meta.get("protected_fields_changed", False)
    return state

def audit_node(state: GFIPGraphState) -> GFIPGraphState:
    state["executed_path"].append("audit")
    # Explanation is now provided by the summary node
    state["audit_reference"] = f"audit-{state['workflow_id']}"
    return state

def route_conditional(state: GFIPGraphState) -> str:
    if state["selected_route"] == "dormant":
        return "followup"
    elif state["selected_route"] == "high_risk":
        return "engagement"
    else:
        return "engagement"

# Graph Builder
def create_graph(use_llm: bool = False):
    workflow = StateGraph(GFIPGraphState)
    
    workflow.add_node("attendance", attendance_node)
    workflow.add_node("router", router_node)
    workflow.add_node("engagement", engagement_risk_node)
    workflow.add_node("trainer", trainer_allocation_node)
    workflow.add_node("followup", followup_recommendation_node)
    workflow.add_node("recommendation", recommendation_node)
    
    if use_llm:
        workflow.add_node("summary", summary_llm_node)
    else:
        workflow.add_node("summary", summary_node)
        
    workflow.add_node("audit", audit_node)
    
    workflow.set_entry_point("attendance")
    workflow.add_edge("attendance", "router")
    
    # Conditional branching
    workflow.add_conditional_edges(
        "router",
        route_conditional,
        {
            "engagement": "engagement",
            "followup": "followup"
        }
    )
    
    # Edges after router
    workflow.add_edge("engagement", "trainer") # Need to handle skip in trainer
    workflow.add_edge("trainer", "followup")
    workflow.add_edge("followup", "recommendation")
    workflow.add_edge("recommendation", "summary")
    workflow.add_edge("summary", "audit")
    workflow.add_edge("audit", END)
    
    return workflow.compile()


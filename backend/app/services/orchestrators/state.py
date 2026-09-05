from typing import TypedDict, List, Any, Optional, Dict

class GFIPGraphState(TypedDict):
    workflow_id: str
    member_id: str
    domain_input: dict[str, Any]
    shared_context: dict[str, Any]
    agent_outputs: List[dict[str, Any]]
    final_recommendation: str
    explanation: Optional[str]
    audit_reference: Optional[str]
    errors: List[str]
    # Routing fields
    route_flags: Dict[str, Any]
    selected_route: str
    route_reason: str
    executed_path: List[str]
    skipped_agents: List[Dict[str, str]]
    # LLM Integration fields
    llm_mode: Optional[str]
    llm_provider: Optional[str]
    llm_model: Optional[str]
    llm_validation_status: Optional[str]
    fallback_used: Optional[bool]
    fallback_reason: Optional[str]
    llm_metadata: Optional[Dict[str, Any]]
    protected_fields_changed: Optional[bool]


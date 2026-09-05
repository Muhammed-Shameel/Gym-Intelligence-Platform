from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LLMSummaryOutput(BaseModel):
    agent_name: str = Field(default="ExplanationSummaryService", description="Name of the agent generating summary")
    mode: str = Field(default="llm_assisted", description="Execution mode")
    summary: str = Field(..., description="Narrative summary for member recommendation")
    observations: List[str] = Field(default_factory=list, description="Key qualitative observations")
    recommendation: str = Field(..., description="Member action recommendation")
    confidence: float = Field(default=0.95, ge=0.0, le=1.0, description="Confidence score")
    risks: List[str] = Field(default_factory=list, description="Identified risk factors")
    missing_information: List[str] = Field(default_factory=list, description="Missing context items")
    protected_fields_changed: bool = Field(default=False, description="Whether protected fields were altered")
    should_fallback: bool = Field(default=False, description="Flag requesting fallback")

class LLMValidationResult(BaseModel):
    is_valid: bool
    status: str  # "passed" or "failed"
    errors: List[str] = Field(default_factory=list)
    protected_fields_violated: bool = False

class LLMAuditMetadata(BaseModel):
    llm_used: bool
    provider: str
    model: str
    validation_status: str
    fallback_used: bool
    fallback_reason: Optional[str] = None
    protected_fields_changed: bool = False
    timestamp: str = ""

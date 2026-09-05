import logging
from datetime import datetime
from typing import Dict, Any, Tuple
from app.application.llm.context_builder import SafeContextBuilder
from app.application.llm.prompt_templates import PromptContract
from app.application.llm.provider_adapter import LLMProviderAdapter
from app.application.llm.validators import LLMOutputValidator
from app.application.llm.schemas import LLMAuditMetadata

logger = logging.getLogger(__name__)

class LLMService:
    """
    Orchestrating Service for LLM Node Integration.
    Manages safe context, prompt contract, provider adapter, output validation, and fallback.
    """
    def __init__(self):
        self.adapter = LLMProviderAdapter()

    def _get_deterministic_fallback(self, safe_context: Dict[str, Any], recommendation: str) -> Dict[str, Any]:
        """
        Deterministic fallback response matching structured output.
        """
        route = safe_context.get("selected_route", "standard")
        attendance = safe_context.get("attendance_metrics", {})
        
        fallback_summary = (
            f"Based on deterministic rule evaluation, member intervention recommendation is: {recommendation}. "
            f"Active route: '{route}'. (Standard explanation generated deterministically)."
        )
        
        return {
            "agent_name": "ExplanationSummaryService",
            "mode": "deterministic_fallback",
            "summary": fallback_summary,
            "observations": [
                f"Selected route: {route}.",
                f"Check-ins (30d): {attendance.get('checkins_last_30_days', 0)}"
            ],
            "recommendation": recommendation,
            "confidence": 1.0,
            "risks": [],
            "missing_information": [],
            "protected_fields_changed": False,
            "should_fallback": True
        }

    def execute_summary_node(self, state: Dict[str, Any], recommendation: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Executes summary node logic with LLM capability and fallback.
        Returns: (output_dict, audit_metadata_dict)
        """
        safe_context = SafeContextBuilder.build_safe_context(state)
        timestamp = datetime.utcnow().isoformat()

        # Check if LLM is enabled
        if not self.adapter.enabled:
            fallback_output = self._get_deterministic_fallback(safe_context, recommendation)
            audit = LLMAuditMetadata(
                llm_used=False,
                provider="none",
                model="none",
                validation_status="skipped",
                fallback_used=True,
                fallback_reason="LLM_ENABLED is set to false",
                protected_fields_changed=False,
                timestamp=timestamp
            )
            return fallback_output, audit.model_dump()

        try:
            # 1. Render Prompt Contract
            prompt = PromptContract.render_prompt(safe_context, recommendation)
            
            # 2. Call LLM via Adapter
            raw_text, effective_provider, effective_model = self.adapter.generate(
                prompt, safe_context, recommendation
            )
            
            # 3. Validate Structured Output & Protected Fields
            val_result, schema_obj = LLMOutputValidator.validate(
                raw_text, safe_context, recommendation
            )
            
            if val_result.is_valid and schema_obj:
                audit = LLMAuditMetadata(
                    llm_used=True,
                    provider=effective_provider,
                    model=effective_model,
                    validation_status=val_result.status,
                    fallback_used=False,
                    fallback_reason=None,
                    protected_fields_changed=False,
                    timestamp=timestamp
                )
                output_dict = schema_obj.model_dump()
                output_dict["mode"] = "llm_assisted"
                return output_dict, audit.model_dump()
            else:
                failure_reason = "; ".join(val_result.errors) if val_result.errors else "Schema validation failed"
                logger.warning(f"LLM validation failed: {failure_reason}. Using deterministic fallback.")
                
                fallback_output = self._get_deterministic_fallback(safe_context, recommendation)
                audit = LLMAuditMetadata(
                    llm_used=True,
                    provider=effective_provider,
                    model=effective_model,
                    validation_status="failed",
                    fallback_used=True,
                    fallback_reason=failure_reason,
                    protected_fields_changed=val_result.protected_fields_violated,
                    timestamp=timestamp
                )
                return fallback_output, audit.model_dump()

        except Exception as e:
            logger.error(f"Unexpected error in LLM Service execution ({e}). Using deterministic fallback.")
            fallback_output = self._get_deterministic_fallback(safe_context, recommendation)
            audit = LLMAuditMetadata(
                llm_used=False,
                provider=self.adapter.provider_name,
                model=self.adapter.model_name,
                validation_status="failed",
                fallback_used=True,
                fallback_reason=f"Execution error: {str(e)}",
                protected_fields_changed=False,
                timestamp=timestamp
            )
            return fallback_output, audit.model_dump()

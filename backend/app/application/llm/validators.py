import json
import logging
from typing import Dict, Any, Tuple
from app.application.llm.schemas import LLMSummaryOutput, LLMValidationResult

logger = logging.getLogger(__name__)

class LLMOutputValidator:
    """
    Validator for LLM Structured Output and Protected Field Verification.
    """
    PROTECTED_FIELDS = [
        "workflow_id", "member_id", "selected_route",
        "route_reason", "audit_reference", "risk_level"
    ]
    POSITIVE_ATTENDANCE_CLAIMS = [
        "regular facility visits",
        "positive engagement indicators",
        "consistent workout schedule",
        "maintains regular",
        "healthy engagement"
    ]
    LOW_ATTENDANCE_CLAIMS = [
        "no check-ins",
        "no recent attendance",
        "low recent attendance",
        "inactive",
        "attendance is low",
        "review"
    ]

    @classmethod
    def validate(cls, raw_output: str, original_context: Dict[str, Any], expected_recommendation: str) -> Tuple[LLMValidationResult, Any]:
        errors = []
        protected_violated = False

        # 1. JSON Parsing Check
        try:
            parsed_data = json.loads(raw_output)
        except Exception as e:
            errors.append(f"Invalid JSON format: {str(e)}")
            return LLMValidationResult(
                is_valid=False,
                status="failed",
                errors=errors,
                protected_fields_violated=False
            ), None

        # 2. Schema Validation via Pydantic
        try:
            schema_obj = LLMSummaryOutput(**parsed_data)
        except Exception as e:
            errors.append(f"Schema validation error: {str(e)}")
            return LLMValidationResult(
                is_valid=False,
                status="failed",
                errors=errors,
                protected_fields_violated=False
            ), None

        # 3. Check for Fallback Request
        if schema_obj.should_fallback:
            errors.append("LLM explicitly requested fallback via output schema.")
            return LLMValidationResult(
                is_valid=False,
                status="failed",
                errors=errors,
                protected_fields_violated=False
            ), schema_obj

        # 4. Protected Fields Protection Check
        if schema_obj.protected_fields_changed:
            protected_violated = True
            errors.append("LLM indicated protected_fields_changed = true.")

        # Check if LLM attempted to modify or contradict protected deterministic route
        if "selected_route" in parsed_data:
            orig_route = original_context.get("selected_route")
            if orig_route and parsed_data["selected_route"] != orig_route:
                protected_violated = True
                errors.append(f"Protected route tampered: expected '{orig_route}', got '{parsed_data['selected_route']}'.")

        # 5. Output Boundaries & Quality Checks
        if len(schema_obj.summary.strip()) < 10:
            errors.append("Summary text is too short or empty.")

        if schema_obj.confidence < 0.0 or schema_obj.confidence > 1.0:
            errors.append(f"Confidence score {schema_obj.confidence} outside range [0.0, 1.0].")

        # 6. Business consistency checks. Passing JSON is not enough; the
        # explanation must match deterministic evidence and recommendations.
        combined_text = " ".join(
            [schema_obj.summary, *schema_obj.observations, *schema_obj.risks, *schema_obj.missing_information]
        ).lower()
        attendance = original_context.get("attendance_metrics", {})
        checkins_last_30_days = attendance.get("checkins_last_30_days")
        trainer = original_context.get("trainer_assignment", {})

        if schema_obj.recommendation != expected_recommendation:
            errors.append(
                f"Recommendation mismatch: expected '{expected_recommendation}', got '{schema_obj.recommendation}'."
            )

        if checkins_last_30_days == 0:
            if any(claim in combined_text for claim in cls.POSITIVE_ATTENDANCE_CLAIMS):
                errors.append("Business consistency error: zero recent attendance cannot be described as regular or positive engagement.")
            if not any(claim in combined_text for claim in cls.LOW_ATTENDANCE_CLAIMS):
                errors.append("Business consistency error: zero recent attendance must be mentioned as low/no attendance or flagged for review.")
            if schema_obj.confidence >= 0.9 and "Maintain current engagement" in expected_recommendation:
                errors.append("Business consistency error: high confidence is not allowed when maintaining engagement despite zero recent attendance.")

        if "Maintain current engagement" in expected_recommendation and checkins_last_30_days and checkins_last_30_days > 0:
            if not any(claim in combined_text for claim in ["regular", "consistent", "check-in", "visit"]):
                errors.append("Business consistency error: maintain-engagement recommendation needs attendance evidence in the explanation.")

        if "Assign new trainer" in expected_recommendation:
            has_active_trainer = trainer.get("has_active_trainer")
            if has_active_trainer is False and not any(term in combined_text for term in ["trainer", "assignment", "assign new trainer"]):
                errors.append("Business consistency error: missing trainer assignment must be explained separately.")

        is_valid = len(errors) == 0 and not protected_violated
        status = "passed" if is_valid else "failed"

        return LLMValidationResult(
            is_valid=is_valid,
            status=status,
            errors=errors,
            protected_fields_violated=protected_violated
        ), schema_obj

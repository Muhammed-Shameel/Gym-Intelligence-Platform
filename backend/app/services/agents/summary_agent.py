import os
import json
try:
    import google.generativeai as genai
except ImportError:
    genai = None
from typing import Any, Dict
from app.services.context.base import SharedWorkflowContext

class SummaryAgent:
    def __init__(self):
        self.name = "ExplanationSummaryService"
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key and genai is not None:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-3.5-flash-lite") # Using flash for speed/cost
        else:
            self.model = None


    def _get_deterministic_fallback(self, context: SharedWorkflowContext, recommendation: str) -> str:
        return f"Based on the deterministic analysis, the recommendation is: {recommendation}. (Standard explanation generated deterministically)."

    def _call_llm(self, context: SharedWorkflowContext, recommendation: str) -> Dict[str, Any]:
        if not self.model:
            raise ValueError("LLM not configured")

        prompt = f"""
        You are {self.name}. Draft a narrative summary for the recommendation: {recommendation}.
        Context: {json.dumps(context.model_dump())}
        Return ONLY valid JSON matching this schema:
        {{
          "summary": "string",
          "observations": ["string"],
          "confidence": 0.95,
          "risks": []
        }}
        """
        response = self.model.generate_content(prompt)
        
        # Parse and validate
        output = json.loads(response.text.replace("```json", "").replace("```", ""))
        
        return {
            "agent_name": self.name,
            "mode": "llm_enhanced",
            "summary": output["summary"],
            "observations": output["observations"],
            "recommendation": recommendation,
            "confidence": output["confidence"],
            "risks": output["risks"],
            "missing_information": [],
            "protected_fields_changed": False,
            "should_fallback": False
        }

    def run(self, context: SharedWorkflowContext, recommendation: str) -> Dict[str, Any]:
        try:
            # Attempt LLM interaction
            if self.model:
                return self._call_llm(context, recommendation)
            else:
                raise ValueError("No API Key configured")
        except Exception as e:
            # Fallback
            return {
                "agent_name": self.name,
                "mode": "deterministic_fallback",
                "summary": self._get_deterministic_fallback(context, recommendation),
                "observations": ["Fallback triggered: " + str(e)],
                "recommendation": recommendation,
                "confidence": 1.0,
                "risks": [],
                "missing_information": [],
                "protected_fields_changed": False,
                "should_fallback": True
            }

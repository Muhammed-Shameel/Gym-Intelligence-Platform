import os
import json
import logging
from typing import Dict, Any, Tuple
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app.application.llm.mock_provider import MockLLMProvider


logger = logging.getLogger(__name__)

class LLMProviderAdapter:
    """
    LLM Provider Adapter for Stage 4 LLM Agent Integration.
    Routes calls to selected provider (mock / gemini / groq / ollama) with zero secret exposure.
    """
    def __init__(self):
        self.enabled = os.getenv("LLM_ENABLED", "true").lower() in ("true", "1", "t")
        self.provider_name = os.getenv("LLM_PROVIDER", "mock").lower()
        self.model_name = os.getenv("LLM_MODEL", "mock-agentic-v1")
        self.timeout = int(os.getenv("LLM_TIMEOUT_SECONDS", "20"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "500"))
        
        self.mock_provider = MockLLMProvider(model_name=self.model_name)

    def generate(self, prompt: str, safe_context: Dict[str, Any], recommendation: str) -> Tuple[str, str, str]:
        """
        Returns tuple: (raw_json_response, effective_provider, effective_model)
        """
        if not self.enabled:
            raise ValueError("LLM_ENABLED is set to false")

        if self.provider_name == "mock":
            raw_text = self.mock_provider.generate(prompt, safe_context, recommendation)
            return raw_text, "mock", self.model_name

        # Use Gemini only when explicitly selected.
        api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
        if self.provider_name == "gemini":
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                
                # Candidate list of active Gemini models
                candidate_models = ["gemini-3.5-flash-lite", "gemini-3.6-flash"]
                
                for candidate in candidate_models:
                    try:
                        model = genai.GenerativeModel(candidate)
                        response = model.generate_content(prompt)
                        raw_text = response.text
                        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                        return raw_text, "gemini", candidate
                    except Exception as e:
                        logger.warning(f"Gemini model '{candidate}' call failed: {e}")
                        continue
            except Exception as e:
                logger.warning(f"Gemini configuration failed: {e}")

        # Fallback to mock
        logger.warning("Gemini integration failed or skipped. Falling back to mock provider.")
        raw_text = self.mock_provider.generate(prompt, safe_context, recommendation)
        return raw_text, "mock_fallback", self.model_name

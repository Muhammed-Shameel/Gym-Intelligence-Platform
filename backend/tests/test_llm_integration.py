import pytest
import json
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.application.llm.provider_adapter import LLMProviderAdapter
from app.application.llm.mock_provider import MockLLMProvider
from app.application.llm.context_builder import SafeContextBuilder
from app.application.llm.prompt_templates import PromptContract
from app.application.llm.validators import LLMOutputValidator
from app.application.llm.llm_service import LLMService

from app.core.database import Base, engine, SessionLocal
from app.data.seed import seed_data

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_data(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)



def test_mock_provider_output():
    """Verify mock provider generates valid JSON matching schema."""
    provider = MockLLMProvider()
    safe_ctx = {
        "selected_route": "standard",
        "attendance_metrics": {"checkins_last_30_days": 12},
        "engagement_risk": {"risk_level": "low"}
    }
    raw_output = provider.generate("prompt", safe_ctx, "Standard Workout Plan")
    parsed = json.loads(raw_output)
    
    assert parsed["agent_name"] == "ExplanationSummaryService"
    assert parsed["mode"] == "llm_assisted"
    assert "Standard Workout Plan" in parsed["recommendation"]
    assert parsed["protected_fields_changed"] is False
    assert parsed["should_fallback"] is False

def test_safe_context_builder():
    """Verify safe context builder extracts minimal context without database credentials."""
    raw_state = {
        "workflow_id": "wf-123",
        "member_id": "mem-456",
        "selected_route": "standard",
        "route_reason": "Standard route",
        "final_recommendation": "Maintain habit",
        "shared_context": {
            "member_profile": {"member_id": "mem-456", "membership_tier": "gold"},
            "attendance_metrics": {"checkins_last_30_days": 8, "days_since_last_checkin": 3},
            "engagement_risk": {"risk_score": 0.2, "risk_level": "low"},
            "db_secret_key": "SUPER_SECRET_KEY_MUST_NOT_EXPOSE"
        },
        "agent_outputs": []
    }
    safe_ctx = SafeContextBuilder.build_safe_context(raw_state)
    
    assert safe_ctx["workflow_id"] == "wf-123"
    assert "db_secret_key" not in safe_ctx
    assert "member_profile" in safe_ctx
    assert safe_ctx["attendance_metrics"]["checkins_last_30_days"] == 8

def test_prompt_contract():
    """Verify prompt contract contains role, boundaries, missing data rules, and schema."""
    safe_ctx = {"selected_route": "standard"}
    prompt = PromptContract.render_prompt(safe_ctx, "Test Rec")
    
    assert "ExplanationSummaryService" in prompt
    assert "STRICT BOUNDARIES" in prompt
    assert "INPUT CONTEXT" in prompt
    assert "Test Rec" in prompt

def test_validator_success():
    """Verify validator passes clean structured output."""
    provider = MockLLMProvider()
    safe_ctx = {"selected_route": "standard"}
    raw_output = provider.generate("prompt", safe_ctx, "Test Rec")
    
    val_res, schema_obj = LLMOutputValidator.validate(raw_output, safe_ctx, "Test Rec")
    assert val_res.is_valid is True
    assert val_res.status == "passed"
    assert schema_obj.protected_fields_changed is False

def test_mock_provider_zero_attendance_uses_low_attendance_evidence():
    """Zero recent check-ins must not be summarized as regular engagement."""
    provider = MockLLMProvider()
    safe_ctx = {
        "selected_route": "standard",
        "attendance_metrics": {
            "checkins_last_30_days": 0,
            "days_since_last_checkin": 45,
            "is_dormant": True,
        },
        "engagement_risk": {"risk_level": "low"},
        "trainer_assignment": {"has_active_trainer": True},
    }

    raw_output = provider.generate("prompt", safe_ctx, "Maintain current engagement")
    parsed = json.loads(raw_output)
    combined_text = " ".join([parsed["summary"], *parsed["observations"]]).lower()

    assert "regular facility visits" not in combined_text
    assert "positive engagement indicators" not in combined_text
    assert "no check-ins" in combined_text or "attendance is low" in combined_text
    assert parsed["confidence"] < 0.9

def test_validator_rejects_zero_attendance_positive_engagement_contradiction():
    """Business validation should reject explanations that contradict attendance evidence."""
    contradictory_json = json.dumps({
        "agent_name": "ExplanationSummaryService",
        "mode": "llm_assisted",
        "summary": "Member maintains regular facility visits with positive engagement indicators.",
        "observations": ["Consistent workout schedule maintained."],
        "recommendation": "Maintain current engagement",
        "confidence": 0.95,
        "risks": [],
        "missing_information": [],
        "protected_fields_changed": False,
        "should_fallback": False
    })
    safe_ctx = {
        "selected_route": "standard",
        "attendance_metrics": {"checkins_last_30_days": 0, "days_since_last_checkin": 35},
        "trainer_assignment": {"has_active_trainer": True},
    }

    val_res, _ = LLMOutputValidator.validate(contradictory_json, safe_ctx, "Maintain current engagement")

    assert val_res.is_valid is False
    assert any("zero recent attendance" in error for error in val_res.errors)

def test_validator_requires_missing_trainer_explanation():
    """Assign-new-trainer recommendations must explain the trainer assignment evidence."""
    missing_trainer_json = json.dumps({
        "agent_name": "ExplanationSummaryService",
        "mode": "llm_assisted",
        "summary": "Member attendance is acceptable and standard monitoring can continue.",
        "observations": ["Recent check-ins support continued engagement."],
        "recommendation": "Maintain current engagement | Assign new trainer",
        "confidence": 0.9,
        "risks": [],
        "missing_information": [],
        "protected_fields_changed": False,
        "should_fallback": False
    })
    safe_ctx = {
        "selected_route": "standard",
        "attendance_metrics": {"checkins_last_30_days": 6, "days_since_last_checkin": 3},
        "trainer_assignment": {"has_active_trainer": False},
    }

    val_res, _ = LLMOutputValidator.validate(
        missing_trainer_json,
        safe_ctx,
        "Maintain current engagement | Assign new trainer",
    )

    assert val_res.is_valid is False
    assert any("trainer assignment" in error for error in val_res.errors)

def test_validator_protected_field_tampering():
    """Verify validator rejects output if protected fields are tampered."""
    tampered_json = json.dumps({
        "agent_name": "ExplanationSummaryService",
        "mode": "llm_assisted",
        "summary": "Malicious summary trying to change route",
        "observations": [],
        "recommendation": "Test Rec",
        "confidence": 0.95,
        "risks": [],
        "missing_information": [],
        "protected_fields_changed": True,  # Flag set to True
        "selected_route": "dormant",       # Tampered route
        "should_fallback": False
    })
    safe_ctx = {"selected_route": "standard"}
    val_res, schema_obj = LLMOutputValidator.validate(tampered_json, safe_ctx, "Test Rec")
    
    assert val_res.is_valid is False
    assert val_res.status == "failed"
    assert val_res.protected_fields_violated is True

def test_llm_service_fallback_on_invalid_json():
    """Verify LLM service falls back to deterministic output if adapter returns invalid JSON."""
    service = LLMService()
    state = {
        "workflow_id": "wf-err",
        "selected_route": "standard",
        "final_recommendation": "Rec",
        "shared_context": {},
        "agent_outputs": []
    }
    
    with patch.object(service.adapter, 'generate', return_value=("NOT_VALID_JSON", "mock", "mock-model")):
        output, audit = service.execute_summary_node(state, "Rec")
        
        assert output["mode"] == "deterministic_fallback"
        assert audit["fallback_used"] is True
        assert audit["validation_status"] == "failed"
        assert "Invalid JSON" in audit["fallback_reason"]

def test_endpoint_parity_deterministic_vs_graph_vs_llm():
    """Verify all 3 endpoints work clean and preserve API contracts."""
    # Fetch members first to get a valid member_id
    res_m = client.get("/api/v1/members")
    assert res_m.status_code == 200
    members = res_m.json()["items"]
    assert len(members) > 0
    m_id = members[0]["id"]


    # 1. Deterministic endpoint
    res_det = client.post(f"/api/v1/reviews/member?member_id={m_id}")
    assert res_det.status_code == 200
    data_det = res_det.json()
    assert "final_recommendation" in data_det
    assert "audit_reference" in data_det

    # 2. LangGraph endpoint
    res_graph = client.post(f"/api/v1/reviews/member-graph?member_id={m_id}")
    assert res_graph.status_code == 200
    data_graph = res_graph.json()
    assert data_graph["graph_mode"] == "langgraph_stateless"
    assert "executed_path" in data_graph
    assert data_graph["fallback_used"] is True

    # 3. LLM-assisted endpoint
    res_llm = client.post(f"/api/v1/reviews/member-llm?member_id={m_id}")
    assert res_llm.status_code == 200
    data_llm = res_llm.json()
    assert data_llm["graph_mode"] == "langgraph_llm_assisted"
    assert data_llm["llm_mode"] in ("llm_assisted", "fallback")
    assert data_llm["llm_provider"] in ("mock", "gemini", "mock_fallback")
    assert data_llm["protected_fields_changed"] is False

def test_llm_adapter_gemini_failure_fallback():
    """Verify LLM Adapter falls back to mock provider if Gemini fails."""
    import os
    with patch.dict(os.environ, {"LLM_PROVIDER": "gemini", "GEMINI_API_KEY": "fake_key"}):
        adapter = LLMProviderAdapter()
        
        with patch.object(adapter.mock_provider, 'generate', return_value="mock_output") as mock_gen:
            # We mock the import of google.generativeai and make it fail
            mock_genai = MagicMock()
            mock_genai.GenerativeModel.return_value.generate_content.side_effect = Exception("Gemini failure")
            with patch.dict('sys.modules', {'google.generativeai': mock_genai}):
                raw_text, provider, model = adapter.generate("prompt", {}, "Rec")
                
                assert provider == "mock_fallback"
                assert raw_text == "mock_output"
                assert mock_gen.called

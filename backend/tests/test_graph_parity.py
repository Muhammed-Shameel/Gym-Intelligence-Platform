import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.domain import Member
from app.data.seed import seed_data
from app.core.database import SessionLocal

@pytest.fixture(autouse=True)
def setup_db(client):
    db = SessionLocal()
    seed_data(db)
    db.close()

def test_graph_vs_deterministic_parity(client):
    db = SessionLocal()
    member = db.query(Member).first()
    # Use member_code which is what the frontend actually uses
    member_id = member.member_code 
    db.close()
    
    # Deterministic workflow
    deterministic_response = client.post(f"/api/v1/reviews/member?member_id={member_id}")
    assert deterministic_response.status_code == 200
    det_data = deterministic_response.json()
    
    # LangGraph workflow
    graph_response = client.post(f"/api/v1/reviews/member-graph?member_id={member_id}")
    assert graph_response.status_code == 200
    graph_data = graph_response.json()
    
    # Compare recommendations
    assert det_data["final_recommendation"] == graph_data["final_recommendation"]
    # Verify graph data contains expected fields
    assert "explanation" in graph_data
    assert "audit_reference" in graph_data

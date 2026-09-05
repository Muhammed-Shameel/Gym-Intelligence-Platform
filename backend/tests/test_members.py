def test_unknown_member_returns_404(client):
    response = client.get("/api/v1/members/UNKNOWN")
    assert response.status_code == 404

from fastapi import status

def test_system_metadata(client):
    response = client.get("/api/v1/system/metadata")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "application" in data["data"]
    assert data["data"]["application"]["name"] == "Ascendrite"
    assert "runtime" in data["data"]
    assert "uptime_seconds" in data["data"]["runtime"]
    assert "python_version" in data["data"]["runtime"]

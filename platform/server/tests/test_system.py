from fastapi import status

def test_system_metadata(client):
    response = client.get("/api/v1/system/metadata")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "success"
    assert "application" in data
    assert data["application"]["name"] == "Ascendrite"
    assert "runtime" in data
    assert "uptime_seconds" in data["runtime"]
    assert "python_version" in data["runtime"]

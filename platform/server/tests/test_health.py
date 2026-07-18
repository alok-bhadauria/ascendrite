from fastapi import status

def test_health_liveness(client):
    response = client.get("/api/v1/health/liveness")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "uptime" in data
    assert "version" in data
    assert "environment" in data
    assert "request_id" in data
    
    # Verify correlation headers
    assert "X-Correlation-ID" in response.headers
    assert "X-Process-Time" in response.headers

def test_health_main(client):
    response = client.get("/api/v1/health")
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE]
    data = response.json()
    
    if response.status_code == status.HTTP_200_OK:
        assert data["status"] == "healthy"
        assert "dependencies" in data
        assert "postgres" in data["dependencies"]
        assert "mongodb" in data["dependencies"]
    else:
        assert data["detail"]["status"] in ["degraded", "unhealthy"]
        assert "dependencies" in data["detail"]

def test_health_readiness(client):
    response = client.get("/api/v1/health/readiness")
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE]

def test_correlation_id_propagation(client):
    correlation_id = "test-custom-correlation-12345"
    response = client.get("/api/v1/health/liveness", headers={"X-Correlation-ID": correlation_id})
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["X-Correlation-ID"] == correlation_id
    assert response.json()["request_id"] == correlation_id

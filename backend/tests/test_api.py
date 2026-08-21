import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from fastapi.testclient import TestClient
from main import app

def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_predict_success():
    with TestClient(app) as client:
        response = client.post("/predict", json={"text": "I have an exam tomorrow and haven't studied at all."})
        assert response.status_code == 200
        data = response.json()
        assert "cooked_score" in data
        assert "cooked_level" in data
        assert "category" in data
        assert "verdict" in data
        assert "recommendations" in data

def test_predict_validation_error():
    with TestClient(app) as client:
        # Text too short
        response = client.post("/predict", json={"text": "no"})
        assert response.status_code == 422

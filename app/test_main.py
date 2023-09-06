from fastapi.testclient import TestClient
from .main import app
from .database import SessionLocal
from .models import Event
from datetime import date


client = TestClient(app)

def test_get_events():
    response = client.get("/")
    assert response.status_code == 200

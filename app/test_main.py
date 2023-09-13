from fastapi.testclient import TestClient
from app.main import app

from app.database import Base, engine, SessionLocal
from app.schemas import Event, EventCreate

client = TestClient(app)



#Tests
def test_get_events_no_filters():
    response = client.get("/")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)
    assert len(events) != 0
    for event in events:
        try:
            event_response = Event.model_validate(event)
        except:
            event_response = None
    assert event_response is not None


def test_get_events_with_checked_filter():
    response = client.get("/?checked=true")
    assert response.status_code == 200
    events = response.json()


def test_get_events_with_event_type_filter():
    response = client.get("/?event_type=commercial")
    assert response.status_code == 200
    events = response.json()


def test_get_events_with_wrong_event_type_filter():
    """422 Unprocessable Entity response is an HTTP status code that indicates that the server understands the request, 
    but it cannot process the request due to semantic errors or validation failures in the request payload"""
    response = client.get("/?event_type=abc")
    assert response.status_code == 422
    events = response.json()    


if __name__ == "__main__":
    import pytest
    pytest.main()
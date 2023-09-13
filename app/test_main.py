from fastapi.testclient import TestClient
from app.main import app

from app.database import Base, engine, SessionLocal
from app.schemas import Event

client = TestClient(app)


############################################   Tests    ############################################

def test_get_events_no_filters():
    response = client.get("/")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list), "Not valid response"
    for event in events:
        try:
            event_response = Event.model_validate(event)
        except:
            event_response = None
        assert event_response is not None, "Wrong json response"


from random import choice

def test_get_events_with_checked_filter():
    checked = choice((0,1))
    response = client.get(f"/?checked={bool(checked)}")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)
    if len(events) != 0:
        for event in events:
            try:
                event_response = Event.model_validate(event)
            except:
                event_response = None
            assert event_response is not None
            assert event["checked"] is bool(checked), "Didn't return correct 'checked' status"


def test_get_events_with_event_type_filter():
    response = client.get("/?event_type=commercial")
    assert response.status_code == 200
    events = response.json()


def test_get_events_with_wrong_event_type_filter():
    response = client.get("/?event_type=abc")
    assert response.status_code == 422
    events = response.json()    


def test_create_event_success():
    event_payload = {
        "name": "Test Event",
        "type": "commercial",
        "description": "This is a test event",
        "event_date": "2023-09-01"
    }

    response = client.post("/create_event", json=event_payload)
    
    assert response.status_code == 200, f"Not valid payload Status-{response.status_code}: {response.json()}"
    
    created_event = response.json()
    
    try:
        event_response = Event.model_validate(created_event)
    except:
        event_response = None
    assert event_response is not None, "Not a valid json response of type Event"


def test_delete_event_success():
    events = client.get("/")
    event_ids = [event["id"] for event in events.json()]
    event_id = choice(event_ids)
    
    response = client.delete(f"/del/{event_id}")

    assert response.status_code == 200
    assert response.json() == {"message": "Event deleted"}


def test_delete_nonexistent_event():
    event_id = 1000
    
    response = client.delete(f"/del/{event_id}")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}


def test_edit_event_success():
    pass


if __name__ == "__main__":
    import pytest
    pytest.main()
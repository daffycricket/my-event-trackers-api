import pytest
from datetime import datetime, timezone
from uuid import uuid4

BASE_URL = "http://localhost:9095/api/events"

def test_create_event(client):
    event_data = {
        "type": "MEAL",
        "date": datetime.now(timezone.utc).isoformat(),
        "data": {"meal_type": "lunch"},
        "notes": "Test meal"
    }
    
    response = client.post(BASE_URL, json=event_data)
    assert response.status_code == 200

def test_get_event(client):
    # D'abord créer un événement
    event_data = {
        "type": "MEAL",
        "date": datetime.now(timezone.utc).isoformat(),
        "data": {"meal_type": "dinner"},
        "notes": "Test dinner"
    }
    
    print("\n----- Test Get Event -----")
    create_url = BASE_URL
    print(f"POST {create_url}")
    print(f"Request body: {event_data}")
    create_response = client.post(create_url, json=event_data)
    print(f"Response status: {create_response.status_code}")
    print(f"Response body: {create_response.text}")
    
    event_id = create_response.json()["id"]
    
    get_url = f"{BASE_URL}/{event_id}"
    print(f"\nGET {get_url}")
    response = client.get(get_url)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    assert response.status_code == 200
    assert response.json()["type"] == "MEAL"
    assert response.json()["notes"] == "Test dinner"

def test_get_nonexistent_event(client):
    random_id = str(uuid4())
    response = client.get(f"{BASE_URL}/{random_id}")
    assert response.status_code == 404

def test_search_events(client):
    # Créer quelques événements
    events = [
        {
            "type": "MEAL",
            "date": datetime.now(timezone.utc).isoformat(),
            "data": {"meal_type": "lunch"},
            "notes": "Test lunch"
        },
        {
            "type": "WORKOUT",
            "date": datetime.now(timezone.utc).isoformat(),
            "data": {"workout_type": "cardio"},
            "notes": "Test workout"
        }
    ]
    
    for event in events:
        client.post(BASE_URL, json=event)
    
    response = client.get(f"{BASE_URL}/search?q=lunch")
    assert response.status_code == 200

def test_list_events(client):
    # Créer plusieurs événements
    events = [
        {
            "type": "MEAL",
            "date": datetime.now(timezone.utc).isoformat(),
            "data": {"meal_type": "breakfast"},
            "notes": "Test breakfast"
        },
        {
            "type": "MEAL",
            "date": datetime.now(timezone.utc).isoformat(),
            "data": {"meal_type": "lunch"},
            "notes": "Test lunch"
        }
    ]
    
    for event in events:
        client.post(BASE_URL, json=event)
    
    response = client.get(BASE_URL)
    assert response.status_code == 200
# Tests des endpoints d'événements

import httpx
from fastapi import status
from datetime import datetime, timezone
from tests.integration import BASE_URLS
import uuid

# Variable globale pour stocker le token
_AUTH_HEADERS = None

def get_auth_headers():
    global _AUTH_HEADERS
    if _AUTH_HEADERS is not None:
        return _AUTH_HEADERS

    with httpx.Client() as client:
        # Créer un utilisateur de test unique
        test_user = {
            "email": f"test_{uuid.uuid4()}@example.com",
            "password": "test123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        try:
            # Essayer de créer l'utilisateur (ignoré si existe déjà)
            client.post(f"{BASE_URLS['auth']}/register", json=test_user)
        except httpx.HTTPStatusError:
            pass
        
        # Login pour obtenir le token
        response = client.post(
            f"{BASE_URLS['auth']}/login",
            data={
                "username": test_user["email"],
                "password": test_user["password"]
            }
        )
        token = response.json()["access_token"]
        _AUTH_HEADERS = {"Authorization": f"Bearer {token}"}
        return _AUTH_HEADERS

def test_create_meal_event():
    with httpx.Client() as client:
        headers = get_auth_headers()
        meal_event_data = {
            "type": "MEAL",
            "date": datetime.now(timezone.utc).isoformat(),
            "notes": "Déjeuner test",
            "data": {"meal_type": "lunch"},
            "meal_items": [
                {"name": "apple", "quantity": 1.0},
                {"name": "banana", "quantity": 1.0}
            ]
        }
        response = client.post(f"{BASE_URLS['events']}", json=meal_event_data, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["type"] == "MEAL"
        assert len(data["meal_items"]) == 2

def test_create_event_unauthorized():
    with httpx.Client() as client:
        meal_event_data = {
            "type": "MEAL",
            "date": datetime.now(timezone.utc).isoformat(),
            "notes": "Test"
        }
        response = client.post(f"{BASE_URLS['events']}", json=meal_event_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_events():
    with httpx.Client() as client:
        headers = get_auth_headers()
        response = client.get(f"{BASE_URLS['events']}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        events = response.json()
        assert isinstance(events, list)

def test_get_single_event():
    with httpx.Client() as client:
        headers = get_auth_headers()
        # Créer un événement
        event_data = {
            "type": "MEAL",
            "date": datetime.now(timezone.utc).isoformat(),
            "notes": "Test"
        }
        create_response = client.post(f"{BASE_URLS['events']}", json=event_data, headers=headers)
        event_id = create_response.json()["id"]
        
        # Récupérer l'événement
        response = client.get(f"{BASE_URLS['events']}/{event_id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == event_id

def test_update_event():
    with httpx.Client() as client:
        headers = get_auth_headers()
        # Créer un événement
        event_data = {
            "type": "MEAL",
            "date": datetime.now(timezone.utc).isoformat(),
            "notes": "Test"
        }
        create_response = client.post(f"{BASE_URLS['events']}", json=event_data, headers=headers)
        event_id = create_response.json()["id"]
        
        # Mettre à jour
        update_data = {"notes": "Updated"}
        response = client.put(f"{BASE_URLS['events']}/{event_id}", json=update_data, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["notes"] == update_data["notes"]

def test_create_workout_event():
    with httpx.Client() as client:
        headers = get_auth_headers()
        workout_event_data = {
            "type": "WORKOUT",
            "date": datetime.now(timezone.utc).isoformat(),
            "notes": "Séance de sport",
            "data": {
                "workout_type": "running",
                "duration": 45,
                "calories_burned": 400
            }
        }
        response = client.post(f"{BASE_URLS['events']}", json=workout_event_data, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["type"] == "WORKOUT"
        assert data["data"]["workout_type"] == "running"
        assert data["data"]["duration"] == 45

def test_create_meal_event_with_invalid_food():
    with httpx.Client() as client:
        headers = get_auth_headers()
        meal_event_data = {
            "type": "MEAL",
            "date": datetime.now(timezone.utc).isoformat(),
            "notes": "Repas test",
            "data": {"meal_type": "lunch"},
            "meal_items": [
                {"name": "nonexistent_food", "quantity": 1.0}
            ]
        }
        response = client.post(f"{BASE_URLS['events']}", json=meal_event_data, headers=headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "detail" in data
        assert "nonexistent_food" in data["detail"]

def test_create_meal_event_with_different_meal_types():
    meal_types = ["breakfast", "lunch", "dinner", "snack"]
    
    with httpx.Client() as client:
        headers = get_auth_headers()
        for meal_type in meal_types:
            meal_event_data = {
                "type": "MEAL",
                "date": datetime.now(timezone.utc).isoformat(),
                "notes": f"Test {meal_type}",
                "data": {"meal_type": meal_type},
                "meal_items": [
                    {"name": "apple", "quantity": 1.0}
                ]
            }
            response = client.post(f"{BASE_URLS['events']}", json=meal_event_data, headers=headers)
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["data"]["meal_type"] == meal_type

def test_create_event_with_invalid_type():
    with httpx.Client() as client:
        headers = get_auth_headers()
        event_data = {
            "type": "INVALID_TYPE",
            "date": datetime.now(timezone.utc).isoformat(),
            "notes": "Test invalide"
        }
        response = client.post(f"{BASE_URLS['events']}", json=event_data, headers=headers)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

def test_create_workout_with_different_types():
    workout_types = ["running", "cycling", "fitness", "strength", "other"]
    
    with httpx.Client() as client:
        headers = get_auth_headers()
        for workout_type in workout_types:
            workout_event_data = {
                "type": "WORKOUT",
                "date": datetime.now(timezone.utc).isoformat(),
                "notes": f"Test {workout_type}",
                "data": {
                    "workout_type": workout_type,
                    "duration": 30,
                    "calories_burned": 300
                }
            }
            response = client.post(f"{BASE_URLS['events']}", json=workout_event_data, headers=headers)
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["data"]["workout_type"] == workout_type

def test_get_events_after_creation():
    with httpx.Client() as client:
        headers = get_auth_headers()
        
        # Créer plusieurs types d'événements
        events_to_create = [
            {
                "type": "MEAL",
                "date": datetime.now(timezone.utc).isoformat(),
                "notes": "Déjeuner test",
                "data": {"meal_type": "lunch"},
                "meal_items": [
                    {"name": "apple", "quantity": 1.0},
                    {"name": "banana", "quantity": 2.0}
                ]
            },
            {
                "type": "WORKOUT",
                "date": datetime.now(timezone.utc).isoformat(),
                "notes": "Course matinale",
                "data": {
                    "workout_type": "running",
                    "duration": 30,
                    "calories_burned": 300
                }
            }
        ]
        
        created_events = []
        for event_data in events_to_create:
            response = client.post(f"{BASE_URLS['events']}", json=event_data, headers=headers)
            assert response.status_code == status.HTTP_200_OK
            created_events.append(response.json())
        
        # Récupérer tous les événements
        response = client.get(f"{BASE_URLS['events']}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        events = response.json()
        
        # Vérifier que nos événements créés sont présents
        for created_event in created_events:
            matching_events = [e for e in events if e["id"] == created_event["id"]]
            assert len(matching_events) == 1
            event = matching_events[0]
            
            # Vérifier les données communes
            assert event["type"] == created_event["type"]
            assert event["notes"] == created_event["notes"]
            assert event["data"] == created_event["data"]
            
            # Vérifier les données spécifiques au type
            if event["type"] == "MEAL":
                assert len(event["meal_items"]) == len(created_event["meal_items"])
                for created_item, retrieved_item in zip(created_event["meal_items"], event["meal_items"]):
                    assert created_item["name"] == retrieved_item["name"]
                    assert created_item["quantity"] == retrieved_item["quantity"]
            elif event["type"] == "WORKOUT":
                assert event["data"]["workout_type"] == created_event["data"]["workout_type"]
                assert event["data"]["duration"] == created_event["data"]["duration"]
                assert event["data"]["calories_burned"] == created_event["data"]["calories_burned"]

def test_get_single_event_details():
    with httpx.Client() as client:
        headers = get_auth_headers()
        
        # Créer un événement repas
        meal_event_data = {
            "type": "MEAL",
            "date": datetime.now(timezone.utc).isoformat(),
            "notes": "Déjeuner détaillé",
            "data": {"meal_type": "lunch"},
            "meal_items": [
                {"name": "apple", "quantity": 1.5},
                {"name": "banana", "quantity": 2.0},
                {"name": "orange", "quantity": 1.0}
            ]
        }
        
        # Créer l'événement
        create_response = client.post(f"{BASE_URLS['events']}", json=meal_event_data, headers=headers)
        assert create_response.status_code == status.HTTP_200_OK
        created_event = create_response.json()
        
        # Récupérer l'événement par son ID
        event_id = created_event["id"]
        response = client.get(f"{BASE_URLS['events']}/{event_id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        retrieved_event = response.json()
        
        # Vérifier tous les détails
        assert retrieved_event["id"] == created_event["id"]
        assert retrieved_event["type"] == "MEAL"
        assert retrieved_event["notes"] == "Déjeuner détaillé"
        assert retrieved_event["data"]["meal_type"] == "lunch"
        assert len(retrieved_event["meal_items"]) == 3
        
        # Vérifier chaque aliment
        expected_items = {
            "apple": 1.5,
            "banana": 2.0,
            "orange": 1.0
        }
        for item in retrieved_event["meal_items"]:
            assert item["name"] in expected_items
            assert item["quantity"] == expected_items[item["name"]]

def test_update_event_details():
    with httpx.Client() as client:
        headers = get_auth_headers()
        
        # 1. Créer un événement initial
        initial_event = {
            "type": "MEAL",
            "date": datetime.now(timezone.utc).isoformat(),
            "notes": "Repas initial",
            "data": {"meal_type": "lunch"},
            "meal_items": [
                {"name": "apple", "quantity": 1.0},
                {"name": "banana", "quantity": 1.0}
            ]
        }
        
        create_response = client.post(f"{BASE_URLS['events']}", json=initial_event, headers=headers)
        assert create_response.status_code == status.HTTP_200_OK
        created_event = create_response.json()
        event_id = created_event["id"]
        
        # 2. Mettre à jour les notes
        notes_update = {
            "notes": "Repas modifié"
        }
        response = client.put(f"{BASE_URLS['events']}/{event_id}", json=notes_update, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        updated_event = response.json()
        assert updated_event["notes"] == "Repas modifié"
        assert updated_event["meal_items"] == created_event["meal_items"]  # Les items n'ont pas changé
        
        # 3. Mettre à jour les meal_items
        items_update = {
            "meal_items": [
                {"name": "orange", "quantity": 2.0},
                {"name": "apple", "quantity": 0.5}
            ]
        }
        response = client.put(f"{BASE_URLS['events']}/{event_id}", json=items_update, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        updated_event = response.json()
        assert len(updated_event["meal_items"]) == 2
        assert any(item["name"] == "orange" and item["quantity"] == 2.0 for item in updated_event["meal_items"])
        assert any(item["name"] == "apple" and item["quantity"] == 0.5 for item in updated_event["meal_items"])
        
        # 4. Mettre à jour les données additionnelles
        data_update = {
            "data": {"meal_type": "dinner"}
        }
        response = client.put(f"{BASE_URLS['events']}/{event_id}", json=data_update, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        updated_event = response.json()
        assert updated_event["data"]["meal_type"] == "dinner"

        # 5. Vérifier l'état final via GET
        get_response = client.get(f"{BASE_URLS['events']}/{event_id}", headers=headers)
        assert get_response.status_code == status.HTTP_200_OK
        final_event = get_response.json()
        
        # Vérifier que toutes les modifications sont présentes
        assert final_event["notes"] == "Repas modifié"
        assert final_event["data"]["meal_type"] == "dinner"
        assert len(final_event["meal_items"]) == 2
        assert any(item["name"] == "orange" and item["quantity"] == 2.0 for item in final_event["meal_items"])
        assert any(item["name"] == "apple" and item["quantity"] == 0.5 for item in final_event["meal_items"])
        assert "banana" not in [item["name"] for item in final_event["meal_items"]]

def test_delete_event():
    with httpx.Client() as client:
        headers = get_auth_headers()
        
        # 1. Créer un événement
        event_data = {
            "type": "WORKOUT",
            "date": datetime.now(timezone.utc).isoformat(),
            "notes": "Séance à supprimer",
            "data": {
                "workout_type": "running",
                "duration": 30,
                "calories_burned": 300
            }
        }
        
        create_response = client.post(f"{BASE_URLS['events']}", json=event_data, headers=headers)
        assert create_response.status_code == status.HTTP_200_OK
        event_id = create_response.json()["id"]
        
        # 2. Vérifier que l'événement existe
        get_response = client.get(f"{BASE_URLS['events']}/{event_id}", headers=headers)
        assert get_response.status_code == status.HTTP_200_OK
        
        # 3. Supprimer l'événement
        delete_response = client.delete(f"{BASE_URLS['events']}/{event_id}", headers=headers)
        assert delete_response.status_code == status.HTTP_200_OK
        
        # 4. Vérifier que l'événement n'existe plus
        get_response = client.get(f"{BASE_URLS['events']}/{event_id}", headers=headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_nonexistent_event():
    with httpx.Client() as client:
        headers = get_auth_headers()
        
        # Essayer de supprimer un événement qui n'existe pas
        response = client.delete(f"{BASE_URLS['events']}/99999", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_nonexistent_event():
    with httpx.Client() as client:
        headers = get_auth_headers()
        
        update_data = {"notes": "Test"}
        response = client.put(f"{BASE_URLS['events']}/99999", json=update_data, headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

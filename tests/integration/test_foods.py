# Tests des endpoints de configuration des aliments

import httpx
from fastapi import status
from tests.integration import BASE_URLS

def test_get_foods_fr():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URLS['foods']}", params={"language": "fr"})
        assert response.status_code == status.HTTP_200_OK
        foods = response.json()
        assert len(foods) > 0
        assert all("label" in food for food in foods)

def test_get_foods_en():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URLS['foods']}", params={"language": "en"})
        assert response.status_code == status.HTTP_200_OK

def test_get_foods_invalid_language():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URLS['foods']}", params={"language": "xx"})
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.text == "Internal Server Error"

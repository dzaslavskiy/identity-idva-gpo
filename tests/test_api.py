"""GPO api tests"""
from fastapi.testclient import TestClient


def test_count_letter(client: TestClient) -> None:
    """test letter count"""
    response = client.get("/letters")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content["count"], int)


def test_create_letter(client: TestClient) -> None:
    """ "create letter"""
    letter = {
        "name": "FAKEY MCFAKERSON",
        "address": "123 FAKE ST",
        "address2": "",
        "city": "GREAT FALLS",
        "state": "MT",
        "zip": "59010",
        "code": "Q82GZBP71C",
        "date": "January 11, 2022",
        "expiry": "January 21, 2022",
        "app": "Example Sinatra App",
        "url": "https://secure.login.gov",
    }
    response = client.post("/letters", json=letter)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content["id"], int)

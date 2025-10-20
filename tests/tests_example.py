import requests

def test_get_users():
    response = requests.get("http://127.0.0.1:5000/users")
    assert response.status_code == 200

def test_create_user():
    data = {"name": "Ana", "email": "ana@example.com"}
    response = requests.post("http://127.0.0.1:5000/users", json=data)
    assert response.status_code == 201

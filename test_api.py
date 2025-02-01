import requests

port = 3004
login_url = f"http://127.0.0.1:{port}/login"
predict_url = f"http://127.0.0.1:{port}/v1/models/lr/predict"

credentials = {
    "username": "user123",
    "password": "password123"
}

valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiZXhwIjoxNzY5ODYyMDU2fQ.hxZrsk48u78_emoHn220GCNNjnIotwEPoEzHicg-zUU"
expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiZXhwIjoxNzM4NDEyMDE3fQ.OVrERiB0j9--uDhb3QYMeTIyn0SrN1FzRkUyVGBKo2k"

def test_missing_token():
    response = requests.get(f"{predict_url}")
    assert response.status_code == 401
    assert response.json().get("detail") == "Missing authentication token"

def test_invalid_token():
    response = requests.get(f"{predict_url}", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401

def test_expired_token():
    response = requests.get(f"{predict_url}", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert response.json().get("detail") == "Token has expired"

def test_valid_token():
    response = requests.get(f"{predict_url}", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200


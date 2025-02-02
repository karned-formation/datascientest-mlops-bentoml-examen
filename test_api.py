import requests

port = 3005
login_url = f"http://127.0.0.1:{port}/login"
predict_url = f"http://127.0.0.1:{port}/v1/models/lr/predict"

credentials = {
    "username": "user123",
    "password": "password123"
}

valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiZXhwIjoxNzY5ODYyMDU2fQ.hxZrsk48u78_emoHn220GCNNjnIotwEPoEzHicg-zUU"
expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiZXhwIjoxNzM4NDEyMDE3fQ.OVrERiB0j9--uDhb3QYMeTIyn0SrN1FzRkUyVGBKo2k"


def test_missing_token():
    response = requests.post(f"{predict_url}")
    assert response.status_code == 401
    assert response.json().get("detail") == "Missing authentication token"


def test_invalid_token():
    response = requests.post(f"{predict_url}", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401


def test_expired_token():
    response = requests.post(f"{predict_url}", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert response.json().get("detail") == "Token has expired"


def test_valid_token():
    response = requests.post(
        f"{predict_url}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "GRE_Score": 307,
            "TOEFL_Score": 108,
            "University_Rating": 2,
            "SOP": 4.0,
            "LOR": 3.5,
            "CGPA": 7.7,
            "Research": 0
        }
    )
    assert response.status_code == 200


def test_valid_prediction():
    response = requests.post(
        f"{predict_url}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "GRE_Score": 307,
            "TOEFL_Score": 108,
            "University_Rating": 2,
            "SOP": 4.0,
            "LOR": 3.5,
            "CGPA": 7.7,
            "Research": 0
        }
    )
    assert response.status_code == 200


def test_invalid_prediction():
    response = requests.post(
        f"{predict_url}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "wrong": 307,
            "data": 108
        }
    )
    assert response.status_code == 400


def test_valid_login():
    response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=credentials
    )
    assert response.status_code == 200
    assert response.json().get("token") is not None


def test_invalid_login():
    response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json={"username": "user123", "password": "wrong_password"}
    )
    assert response.status_code == 500

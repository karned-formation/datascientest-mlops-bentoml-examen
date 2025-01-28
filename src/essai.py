import requests

login_url = "http://127.0.0.1:3003/login"
predict_url = "http://127.0.0.1:3003/v1/models/lr/predict"

credentials = {
    "username": "user123",
    "password": "password123"
}

login_response = requests.post(
    login_url,
    headers={"Content-Type": "application/json"},
    json=credentials
)

if login_response.status_code == 200:
    token = login_response.json().get("token")

    data = {
    "GRE_Score": 307,
    "TOEFL_Score": 108,
    "University_Rating": 2,
    "SOP": 4.0,
    "LOR": 3.5,
    "CGPA": 7.7,
    "Research": 0
    }

    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=data
    )

    print("Réponse de l'API de prédiction:", response.text)
else:
    print("Erreur lors de la connexion:", login_response.text)
from datetime import datetime, timedelta
import jwt
from config import JWT_ALGORITHM, JWT_SECRET_KEY


def create_jwt_token( user_id: str ):
    expiration = datetime.utcnow() + timedelta(weeks=52)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token
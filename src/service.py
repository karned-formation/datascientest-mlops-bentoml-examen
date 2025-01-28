import joblib
import bentoml
import pandas as pd
from bentoml.io import JSON
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from datetime import datetime, timedelta

JWT_SECRET_KEY = "your_jwt_secret_key_here"
JWT_ALGORITHM = "HS256"

USERS = {
    "user123": "password123",
    "user456": "password456"
}

scaler = joblib.load('../models/scaler_std.pkl')


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch( self, request, call_next ):
        if request.url.path == "/v1/models/lr/predict":
            token = request.headers.get("Authorization")
            if not token:
                return JSONResponse(status_code=401, content={"detail": "Missing authentication token"})

            try:
                token = token.split()[1]  # Remove 'Bearer ' prefix
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

            request.state.user = payload.get("sub")

        response = await call_next(request)
        return response


class InputModel(BaseModel):
    GRE_Score: int
    TOEFL_Score: int
    University_Rating: float
    SOP: float
    LOR: float
    CGPA: float
    Research: int


linear_regression_runner = bentoml.sklearn.get("linear_regression:qnxg6mg5j6gkotsj").to_runner()

lr_service = bentoml.Service("lr_service", runners=[linear_regression_runner])

lr_service.add_asgi_middleware(JWTAuthMiddleware)


@lr_service.api(input=JSON(), output=JSON())
def login( credentials: dict ) -> dict:
    username = credentials.get("username")
    password = credentials.get("password")

    if username in USERS and USERS[username] == password:
        token = create_jwt_token(username)
        return {"token": token}
    else:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})


@lr_service.api(
    input=JSON(pydantic_model=InputModel),
    output=JSON(),
    route='v1/models/lr/predict'
)
async def classify(input_data: InputModel) -> dict:
    df = pd.DataFrame([input_data.model_dump()])
    df = df.rename(
        columns={
            "GRE_Score": "GRE Score",
            "TOEFL_Score": "TOEFL Score",
            "University_Rating": "University Rating",
            "LOR": "LOR "
        }
    )
    colonnes = ['GRE Score', 'TOEFL Score', 'CGPA']
    scaler_std = joblib.load('../models/scaler_std.pkl')
    df[colonnes] = scaler_std.transform(df[colonnes])
    result = await linear_regression_runner.predict.async_run(df)

    return {
        "prediction": result.tolist()
    }


def create_jwt_token( user_id: str ):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

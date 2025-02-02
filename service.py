import logging

import joblib
import bentoml
import pandas as pd
from bentoml.io import JSON

from config import USERS
from middleware.token_middleware import JWTAuthMiddleware
from models.credential_model import CredentialModel
from models.input_model import InputModel
from models.response_model import ResponseModel
from models.response_token_model import ResponseTokenModel
from src.token import create_jwt_token
from starlette.responses import JSONResponse

logging.basicConfig(level=logging.INFO)

scaler_std = joblib.load("scaler_std.pkl")

linear_regression_runner = bentoml.sklearn.get("linear_regression:qnxg6mg5j6gkotsj").to_runner()
lr_service = bentoml.Service("lr_service", runners=[linear_regression_runner])
lr_service.add_asgi_middleware(JWTAuthMiddleware)


@lr_service.api(
    input=JSON(pydantic_model=CredentialModel),
    output=JSON(pydantic_model=ResponseTokenModel),
    route='login'
)
def login( credentials: CredentialModel ) -> dict:
    logging.info('######################## je suis là')
    if credentials.username in USERS and USERS[credentials.username] == credentials.password:
        token = create_jwt_token(credentials.username)
        return {"token": token}
    else:
        logging.info('######################## je suis ici')
        return JSONResponse(status_code=401, content={"detail": "Invalid credential"})


@lr_service.api(
    input=JSON(pydantic_model=InputModel),
    output=JSON(pydantic_model=ResponseModel),
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
    scaler_std = joblib.load('scaler_std.pkl')
    df[colonnes] = scaler_std.transform(df[colonnes])
    result = await linear_regression_runner.predict.async_run(df)

    return {
        "prediction": result[0][0]
    }




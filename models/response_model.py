from pydantic import BaseModel

class ResponseModel(BaseModel):
    prediction: float
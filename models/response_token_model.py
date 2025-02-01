from pydantic import BaseModel

class ResponseTokenModel(BaseModel):
    token: str
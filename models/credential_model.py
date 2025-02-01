from pydantic import BaseModel

class CredentialModel(BaseModel):
    username: str
    password: str
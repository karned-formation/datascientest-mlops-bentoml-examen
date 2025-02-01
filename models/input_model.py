from pydantic import BaseModel

class InputModel(BaseModel):
    GRE_Score: int
    TOEFL_Score: int
    University_Rating: float
    SOP: float
    LOR: float
    CGPA: float
    Research: int
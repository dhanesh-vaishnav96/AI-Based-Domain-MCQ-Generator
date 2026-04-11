from pydantic import BaseModel, Field
from enum import Enum



class MCQRequest(BaseModel):
    domain: str = Field(..., example="Python")
    difficulty: str = Field(..., example="Hard")
    num_questions: int = Field(..., gt=0, lt=200)
    
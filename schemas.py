from pydantic import BaseModel, Field
from typing import List

class UserProfileCreate(BaseModel):
    age: int = Field(gt=0, lt=120)
    height_feet: int = Field(ge=1, le=8)
    height_inches: int = Field(ge=0, le=11)
    weight: float = Field(ge=40.0, le=1000.0)
    gender: str

    goal: str
    dietary_preferences: List[str] = []
    allergies: List[str] = []
    medical_conditions: List[str] = []

    budget_level: float
    cooking_time: str

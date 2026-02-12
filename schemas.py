from pydantic import BaseModel, Field
from typing import List

class UserProfileCreate(BaseModel):
    age: int = Field(gt=0, lt=120)
    height_cm: float = Field(ge=50)
    weight_kg: float = Field(ge=20)
    gender: str

    goal: str
    dietary_preferences: List[str] = []
    allergies: List[str] = []
    medical_conditions: List[str] = []

    budget_level: str
    cooking_time: str

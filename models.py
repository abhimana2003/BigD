from sqlalchemy import Column, Integer, String, Float, ARRAY
from database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    gender = Column(String, nullable=False)

    goal = Column(String, nullable=False)
    dietary_preferences = Column(ARRAY(String))
    allergies = Column(ARRAY(String))
    medical_conditions = Column(ARRAY(String))

    budget_level = Column(String)
    cooking_time = Column(String)

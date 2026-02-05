from sqlalchemy.orm import Session
from models import UserProfile
from schemas import UserProfileCreate

def create_user_profile(db: Session, profile: UserProfileCreate):
    db_profile = UserProfile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_user_profiles(db: Session):
    return db.query(UserProfile).all()


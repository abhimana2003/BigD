from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, schemas

app = FastAPI(title="Nutrition AI User Profiling API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/profiles")
def create_profile(profile: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    return crud.create_user_profile(db, profile)

@app.get("/profiles")
def list_profiles(db: Session = Depends(get_db)):
    return crud.get_user_profiles(db)

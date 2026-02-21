from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter()

@router.get("/")
def dashboard_home(db: Session = Depends(get_db)):
    return {"message": "DB Connected Successfully"}
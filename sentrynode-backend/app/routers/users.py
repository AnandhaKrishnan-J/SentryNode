from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.services import user_service

router = APIRouter()


@router.post("/register")
def register(payload: UserRegister, db: Session = Depends(get_db)):
    return user_service.register_user(db, payload)


# Register body
# {
#   "username": "admin1",
#   "email": "admin1@example.com",
#   "password": "StrongPassword123"
# }


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return user_service.login_user(db, payload)
#Login Body
# {
#   "username": "admin1",
#   "password": "Password123"
# }
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    role = Column(String, default="analyst")  # admin / analyst
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)


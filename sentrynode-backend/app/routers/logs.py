from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services import logs_service
from app.schemas.logs import TrafficLogListResponse

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("", response_model=TrafficLogListResponse)
def get_traffic_logs(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total, items = logs_service.list_traffic_logs(db, current_user, limit, offset)
    return {
        "total": total,
        "items": items
    }

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services import dashboard_service
from app.schemas.dashboard import DashboardSummary


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return dashboard_service.get_dashboard_summary(db, current_user)
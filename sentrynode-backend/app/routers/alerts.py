from fastapi import APIRouter, Query, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.alert import Alert, AlertListResponse, AlertCreate
from app.services import alert_service
from app.core.security import get_current_user
from app.models.user import User


#Protected Router
protected_router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

#Public router
public_router = APIRouter()



@protected_router.get("", response_model=AlertListResponse)
def list_alerts(
    severity: str | None = Query(None),
    resolved: bool | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    total, alerts = alert_service.list_alerts(db, severity, resolved, limit, offset)

    return {
        "total": total,
        "alerts": alerts
    }


@protected_router.get("/{alert_id}", response_model=Alert)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    return alert_service.get_alert_by_id(db, alert_id)


    return alert_service.acknowledge_alert(db, alert_id)


@protected_router.post("/clear-all")
def clear_all_alerts(
    db: Session = Depends(get_db),
):
    return alert_service.clear_all_alerts(db)


#public 
@public_router.post("", response_model=Alert, status_code=status.HTTP_201_CREATED)
def create_alert(
    payload: AlertCreate,
    db: Session = Depends(get_db),
):
    return alert_service.create_alert(db, payload)
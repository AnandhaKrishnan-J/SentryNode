from fastapi import APIRouter, Query, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models import Alert as AlertModel
from app.schemas.alert import Alert, AlertListResponse

router = APIRouter()


@router.get("", response_model=AlertListResponse)
def list_alerts(
    severity: str | None = Query(None, description="LOW, MEDIUM, HIGH"),
    resolved: bool | None = Query(None, description="true or false"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Returns filtered, paginated list of alerts from database.
    """

    query = db.query(AlertModel)

    # Apply filters
    if severity:
        query = query.filter(AlertModel.severity == severity)

    if resolved is not None:
        query = query.filter(AlertModel.resolved == resolved)

    total = query.count()

    alerts = (
        query
        .order_by(AlertModel.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "alerts": alerts
    }


@router.get("/{alert_id}", response_model=Alert)
def get_alert(alert_id: str, db: Session = Depends(get_db)):
    """
    Returns full details for a single alert.
    """

    alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )

    return alert


@router.patch("/{alert_id}/acknowledge", response_model=Alert)
def acknowledge_alert(alert_id: str, db: Session = Depends(get_db)):
    """
    Marks an alert as resolved (acknowledged).
    """

    alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )

    if alert.resolved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alert already acknowledged"
        )

    alert.resolved = True
    db.commit()
    db.refresh(alert)

    return alert
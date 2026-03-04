from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.alert import Alert
from app.models.device import Device


def list_alerts(db: Session, severity: str | None, resolved: bool | None, limit: int, offset: int):
    query = db.query(Alert)

    if severity:
        query = query.filter(Alert.severity == severity.upper())

    if resolved is not None:
        query = query.filter(Alert.resolved == resolved)

    total = query.count()

    alerts = (
        query
        .order_by(Alert.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, alerts


def get_alert_by_id(db: Session, alert_id: int):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )

    return alert


def acknowledge_alert(db: Session, alert_id: int):
    alert = get_alert_by_id(db, alert_id)

    if alert.resolved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alert already acknowledged"
        )

    alert.resolved = True
    db.commit()
    db.refresh(alert)

    return alert


def create_alert(db: Session, payload):
    # Validate device exists
    device = db.query(Device).filter(
        Device.device_identifier == payload.device_identifier
    ).first()

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not registered"
        )

    new_alert = Alert(
        device_id=device.id,
        alert_type=payload.alert_type,
        severity=payload.severity,
        description=payload.description,
        source_ip=payload.source_ip,
        destination_ip=payload.destination_ip,
        protocol=payload.protocol,
        confidence_score=payload.confidence_score
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert


def clear_all_alerts(db: Session):
    unresolved = db.query(Alert).filter(Alert.resolved == False).all()
    for alert in unresolved:
        alert.resolved = True
    db.commit()
    return {"message": f"Cleared {len(unresolved)} alerts"}
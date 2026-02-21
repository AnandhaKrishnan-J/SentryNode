from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models.device import Device


def create_device(db: Session, payload, current_user):
    existing = db.query(Device).filter(
        Device.device_identifier == payload.device_identifier
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device identifier already exists"
        )

    device = Device(
        device_name=payload.device_name,
        device_identifier=payload.device_identifier,
        location=payload.location,
        ip_address=payload.ip_address,
        owner_id=current_user.id
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return device


def list_devices(db: Session, current_user, limit: int, offset: int):
    query = db.query(Device).filter(Device.owner_id == current_user.id)

    total = query.count()

    devices = (
        query
        .order_by(Device.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, devices


def get_device(db: Session, device_id: int, current_user):
    device = db.query(Device).filter(
        Device.id == device_id,
        Device.owner_id == current_user.id
    ).first()

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )

    return device


def update_last_seen(db: Session, device_identifier: str):
    device = db.query(Device).filter(
        Device.device_identifier == device_identifier
    ).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not registered")

    device.last_seen = datetime.now(timezone.utc)
    device.status = "online"

    db.commit()
    db.refresh(device)

    return device
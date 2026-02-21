from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.device import DeviceCreate, DeviceResponse, DeviceListResponse
from app.services import device_service
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(
    payload: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return device_service.create_device(db, payload, current_user)

#Device
#Header:
# Authorization : Bearer <Token> (from login response)
# Body:
# {
#   "device_name": "Pi-Node-1",
#   "device_identifier": "pi-node-001",
#   "location": "Lab-1",
#   "ip_address": "192.168.1.10"
# }

@router.get("", response_model=DeviceListResponse)
def list_devices(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total, devices = device_service.list_devices(db, current_user, limit, offset)

    return {
        "total": total,
        "devices": devices
    }


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return device_service.get_device(db, device_id, current_user)
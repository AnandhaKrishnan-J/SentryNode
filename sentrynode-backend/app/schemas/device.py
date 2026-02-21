from pydantic import BaseModel
from datetime import datetime


class DeviceBase(BaseModel):
    device_name: str
    device_identifier: str
    location: str | None = None
    ip_address: str | None = None


class DeviceCreate(DeviceBase):
    pass


class DeviceResponse(DeviceBase):
    id: int
    status: str
    last_seen: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True


class DeviceListResponse(BaseModel):
    total: int
    devices: list[DeviceResponse]
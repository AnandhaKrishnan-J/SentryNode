from pydantic import BaseModel
from datetime import datetime
from typing import List, Literal


class DeviceHealth(BaseModel):
    device_id: int
    device_name: str
    status: Literal["online", "offline"]
    last_seen: datetime | None
    cpu_usage: float | None
    memory_usage: float | None
    packet_rate: float | None


class RecentAlert(BaseModel):
    id: int
    alert_type: str
    severity: str
    timestamp: datetime
    resolved: bool

    class Config:
        from_attributes = True


class DashboardSummary(BaseModel):
    security_status: Literal["SAFE", "UNDER_ATTACK", "DEGRADED"]
    active_alerts: int
    highest_severity: str | None
    last_attack_time: datetime | None
    devices: List[DeviceHealth]
    recent_alerts: List[RecentAlert]
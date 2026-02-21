from pydantic import BaseModel
from typing import Literal, List
from datetime import datetime


class DashboardSummary(BaseModel):
    security_status: Literal["SAFE", "UNDER_ATTACK"]
    active_alerts: int
    highest_severity: Literal["LOW", "MEDIUM", "HIGH"]
    last_attack_time: datetime | None
    system_health: Literal["ONLINE", "DEGRADED", "OFFLINE"]


class RecentAlert(BaseModel):
    alert_id: str
    timestamp: datetime
    attack_type: str
    severity: Literal["LOW", "MEDIUM", "HIGH"]
    source_ip: str
    status: Literal["NEW", "ACKNOWLEDGED"]


class RecentAlertsResponse(BaseModel):
    alerts: List[RecentAlert]

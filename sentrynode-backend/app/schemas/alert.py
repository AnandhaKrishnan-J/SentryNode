from pydantic import BaseModel, ConfigDict
from typing import List, Literal
from datetime import datetime


class Alert(BaseModel):
    id: str
    device_id: str
    alert_type: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    description: str | None = None
    source_ip: str | None = None
    destination_ip: str | None = None
    protocol: str | None = None
    confidence_score: float | None = None
    timestamp: datetime
    resolved: bool

    model_config = ConfigDict(from_attributes=True)


class AlertListResponse(BaseModel):
    total: int
    alerts: List[Alert]
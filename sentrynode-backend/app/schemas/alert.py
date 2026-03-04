from pydantic import BaseModel, ConfigDict
from typing import List, Literal, Optional
from datetime import datetime


# ==========================================================
# Incoming payload (used by POST /alerts)
# ==========================================================
class AlertCreate(BaseModel):
    device_identifier: str
    alert_type: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    description: Optional[str] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    protocol: Optional[str] = None
    confidence_score: Optional[float] = None


# ==========================================================
# Outgoing single alert response
# Used by:
#   GET /alerts/{id}
#   PATCH /alerts/{id}/acknowledge
#   POST /alerts
# ==========================================================
class Alert(BaseModel):
    id: int
    device_id: int
    alert_type: str
    severity: str
    description: Optional[str]
    source_ip: Optional[str]
    destination_ip: Optional[str]
    protocol: Optional[str]
    confidence_score: Optional[float]
    timestamp: datetime
    resolved: bool

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Paginated response for GET /alerts
# ==========================================================
class AlertListResponse(BaseModel):
    total: int
    alerts: List[Alert]


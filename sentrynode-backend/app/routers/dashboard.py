from fastapi import APIRouter
from datetime import datetime, timezone

from app.schemas.dashboard import (
    DashboardSummary,
    RecentAlert,
    RecentAlertsResponse
)

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary():
    return {
        "security_status": "UNDER_ATTACK",
        "active_alerts": 3,
        "highest_severity": "HIGH",
        "last_attack_time": datetime.now(timezone.utc),
        "system_health": "ONLINE"
    }


@router.get("/recent-alerts", response_model=RecentAlertsResponse)
def get_recent_alerts(limit: int = 5):
    alerts = [
        {
            "alert_id": "a1f93c",
            "timestamp": datetime.now(timezone.utc),
            "attack_type": "DoS",
            "severity": "HIGH",
            "source_ip": "192.168.1.24",
            "status": "NEW"
        },
        {
            "alert_id": "b7k21d",
            "timestamp": datetime.now(timezone.utc),
            "attack_type": "Port Scan",
            "severity": "MEDIUM",
            "source_ip": "192.168.1.17",
            "status": "NEW"
        }
    ]

    return {
        "alerts": alerts[:limit]
    }

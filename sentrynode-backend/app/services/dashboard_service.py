from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.alert import Alert
from app.models.device import Device
from app.models.system_metric import SystemMetric


ONLINE_THRESHOLD_SECONDS = 60


def get_dashboard_summary(db: Session, current_user):

    now = datetime.now(timezone.utc)


    unresolved_alerts = db.query(Alert).filter(
        Alert.resolved == False
    )

    active_alerts_count = unresolved_alerts.count()

    highest_severity = None
    last_attack_time = None

    severity_order = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    alerts_list = unresolved_alerts.order_by(desc(Alert.timestamp)).all()

    if alerts_list:
        last_attack_time = alerts_list[0].timestamp

        highest = max(
            alerts_list,
            key=lambda a: severity_order.index(a.severity)
        )
        highest_severity = highest.severity


    devices = db.query(Device).filter(
        Device.owner_id == current_user.id
    ).all()

    device_health_data = []

    any_device_offline = False

    for device in devices:

        # Determine online/offline
        if device.last_seen and (now - device.last_seen) <= timedelta(seconds=ONLINE_THRESHOLD_SECONDS):
            status = "online"
        else:
            status = "offline"
            any_device_offline = True

        # Get latest metric
        latest_metric = db.query(SystemMetric).filter(
            SystemMetric.device_id == device.id
        ).order_by(desc(SystemMetric.timestamp)).first()

        device_health_data.append({
            "device_id": device.id,
            "device_name": device.device_name,
            "status": status,
            "last_seen": device.last_seen,
            "cpu_usage": latest_metric.cpu_usage if latest_metric else None,
            "memory_usage": latest_metric.memory_usage if latest_metric else None,
            "packet_rate": latest_metric.packet_rate if latest_metric else None,
        })


    if highest_severity in ["CRITICAL", "HIGH"] and active_alerts_count > 0:
        security_status = "UNDER_ATTACK"
    elif any_device_offline:
        security_status = "DEGRADED"
    else:
        security_status = "SAFE"


    recent_alerts = db.query(Alert).order_by(
        desc(Alert.timestamp)
    ).limit(5).all()

    return {
        "security_status": security_status,
        "active_alerts": active_alerts_count,
        "highest_severity": highest_severity,
        "last_attack_time": last_attack_time,
        "devices": device_health_data,
        "recent_alerts": recent_alerts
    }
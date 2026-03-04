import requests
from datetime import datetime, timezone
from app.config import settings

ALERT_ENDPOINT = f"{settings.BACKEND_URL}/api/alerts"

def send_alert(
    source_ip,
    destination_ip,
    protocol,
    error,
    description="ML anomaly detected"
):
    payload = {
        "device_identifier": settings.DEVICE_ID,
        "alert_type": "ML_ANOMALY",
        "severity": "HIGH",
        "description": description,
        "source_ip": source_ip,
        "destination_ip": destination_ip,
        "protocol": protocol,
        "confidence_score": float(error),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        response = requests.post(ALERT_ENDPOINT, json=payload, timeout=5)
        print(f"Alert sent to backend | status={response.status_code}")
    except Exception as e:
        print("Failed to send alert:", e)
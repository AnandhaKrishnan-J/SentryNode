import requests
from datetime import datetime, timezone
from app.config import settings

ALERT_ENDPOINT = f"{settings.BACKEND_URL}/alerts"

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
        "confidence_score": float(error)
    }

    try:
        response = requests.post(ALERT_ENDPOINT, json=payload, timeout=5)

        if response.status_code == 201:
            print("✅ Alert stored in backend")
        else:
            print("❌ Alert failed:", response.status_code, response.text)

    except Exception as e:
        print("Alert send failed:", e)
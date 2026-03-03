import requests
from datetime import datetime, timezone
from config import settings

def send_alert(flow, error):

    payload = {
        "type": "ML_ANOMALY",
        "source_ip": flow.get("src_ip", "unknown"),
        "severity": "HIGH",
        "details": f"Reconstruction error: {error}",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        requests.post(settings.BACKEND_URL + "/api/alerts", json=payload, timeout=5)
    except Exception as e:
        print("Alert send failed:", e)
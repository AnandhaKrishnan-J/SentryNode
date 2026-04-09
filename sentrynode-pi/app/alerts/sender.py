import queue
from app.config import settings
from app.network.session import session


ALERT_ENDPOINT = f"{settings.BACKEND_URL}/alerts"

alert_queue = queue.Queue()


def get_severity(error, threshold):
    score = error / threshold

    if score < 2:
        return "LOW"
    elif score < 5:
        return "MEDIUM"
    elif score < 15:
        return "HIGH"
    else:
        return "CRITICAL"
    
def send_alert(features, error, threshold, description="ML anomaly detected"):

    alert_queue.put((features, error, threshold, description))

def alert_worker():
    while True:
        features, error, threshold, description = alert_queue.get()

        severity = get_severity(error, threshold)

        payload = {
            "device_identifier": settings.DEVICE_ID,
            "alert_type": "ML_ANOMALY",
            "severity": severity,
            "description": description,
            "source_ip": features.get("src_ip"),
            "destination_ip": features.get("dst_ip"),
            "protocol": features.get("proto"),
            "confidence_score": float(error)
        }

        try:
            response = session.post(ALERT_ENDPOINT, json=payload, timeout=5)

            if response.status_code == 201:
                print("✅ Alert stored")
            else:
                print("❌ Alert failed:", response.status_code)

        except Exception as e:
            print("Alert send failed:", e)

        alert_queue.task_done()
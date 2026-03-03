import time
import requests
import psutil
from datetime import datetime, timezone
from config import settings

def send_heartbeat():

    payload = {
        "device_id": settings.DEVICE_ID,
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        response = requests.post(
            f"{settings.BACKEND_URL}/devices/heartbeat",
            json=payload,
            timeout=5
        )

        print("Heartbeat sent:", response.status_code)

    except Exception as e:
        print("Heartbeat failed:", e)


def heartbeat_loop():
    while True:
        send_heartbeat()
        time.sleep(settings.HEARTBEAT_INTERVAL)
import time
import requests
import psutil
import logging
from datetime import datetime, timezone

from app.config import settings


def send_heartbeat():

    payload = {
        "device_id": settings.DEVICE_ID,
        "cpu_usage": psutil.cpu_percent(interval=0.5),
        "memory_usage": psutil.virtual_memory().percent,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        response = requests.post(
            settings.HEARTBEAT_ENDPOINT,
            json=payload,
            timeout=settings.ALERT_TIMEOUT
        )

        logging.info(f"Heartbeat sent | status={response.status_code}")

    except Exception as e:
        logging.error(f"Heartbeat failed: {e}")


def heartbeat_loop():
    while True:
        send_heartbeat()
        time.sleep(settings.HEARTBEAT_INTERVAL)
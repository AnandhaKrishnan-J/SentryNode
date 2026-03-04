import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    # ===== Network =====
    INTERFACE = os.getenv("INTERFACE", "eth0")

    # ===== Backend =====
    BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/api")

    ALERT_ENDPOINT = f"{BACKEND_URL}/api/alerts"
    HEARTBEAT_ENDPOINT = f"{BACKEND_URL}/api/devices/heartbeat"

    DEVICE_ID = os.getenv("DEVICE_ID", "pi-node-002")

    # ===== Heartbeat =====
    HEARTBEAT_INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", 15))

    # ===== Alerts =====
    ALERT_TIMEOUT = int(os.getenv("ALERT_TIMEOUT", 5))

    # ===== Detection =====
    FLOW_TIMEOUT = int(os.getenv("FLOW_TIMEOUT", 10))


settings = Settings()
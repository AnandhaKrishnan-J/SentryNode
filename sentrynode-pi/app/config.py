import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    # ===== Network =====
    INTERFACE = os.getenv("INTERFACE", "wlan0")

    # ===== Backend =====
    BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    DEVICE_ID = os.getenv("DEVICE_ID", "pi-node-001")

    # ===== Heartbeat =====
    HEARTBEAT_INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", 15))

    # ===== Alerts =====
    ALERT_TIMEOUT = int(os.getenv("ALERT_TIMEOUT", 5))

    # ===== Detection =====
    PORT_SCAN_THRESHOLD = int(os.getenv("PORT_SCAN_THRESHOLD", 50))
    FLOW_TIMEOUT = int(os.getenv("FLOW_TIMEOUT", 10))

settings = Settings()
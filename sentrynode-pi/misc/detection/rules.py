from app.config import settings
from collections import defaultdict
import time

connection_tracker = defaultdict(list)

def detect_port_scan(packet):
    src = packet["src_ip"]
    dst_port = packet["dst_port"]

    current_time = time.time()

    connection_tracker[src].append((dst_port, current_time))

    # Remove old entries (10 second window)
    connection_tracker[src] = [
        (port, t) for port, t in connection_tracker[src]
        if current_time - t < 10
    ]

    unique_ports = len(set([port for port, _ in connection_tracker[src]]))

    if unique_ports > settings.PORT_SCAN_THRESHOLD:
        return {
            "type": "PORT_SCAN",
            "source_ip": src,
            "severity": "HIGH",
            "details": f"{unique_ports} unique ports scanned"
        }

    return None


def detect_large_packet(packet):
    if packet["packet_size"] > 1500:
        return {
            "type": "LARGE_PACKET",
            "source_ip": packet["src_ip"],
            "severity": "MEDIUM",
            "details": "Packet size exceeded threshold"
        }
    return None


def detect_suspicious_port(packet):
    suspicious_ports = [22, 23, 3389]

    if packet["dst_port"] in suspicious_ports:
        return {
            "type": "SUSPICIOUS_PORT_ACCESS",
            "source_ip": packet["src_ip"],
            "severity": "MEDIUM",
            "details": f"Access attempt to port {packet['dst_port']}"
        }
    return None
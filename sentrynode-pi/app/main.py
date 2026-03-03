import threading
from app.sniffer.capture import start_sniffing
from app.flow.aggregator import update_flow, expire_flows
from app.ml.detector import detect
from app.alerts.sender import send_alert
from app.heartbeat import heartbeat_loop

def handle_packet(pkt):

    update_flow(pkt)

    expired = expire_flows()

    for key, flow in expired:

        flow_dict = {
            "proto": key[4],
            "service": "http",  # temporary
            "state": "CON",     # temporary
            "dur": flow["last_seen"] - flow["start_time"],
            "sbytes": flow["sbytes"],
            "dbytes": 0,
            "spkts": flow["spkts"],
            "dpkts": 0,
            "sload": 0,
            "dload": 0,
            "sjit": 0,
            "djit": 0,
            "sinpkt": 0,
            "dinpkt": 0,
            "tcprtt": 0,
            "synack": 0,
            "ackdat": 0,
        }

        is_anomaly, error = detect(flow_dict)

        if is_anomaly:
            send_alert(flow_dict, error)

def main():

    threading.Thread(target=heartbeat_loop, daemon=True).start()

    start_sniffing(handle_packet)

if __name__ == "__main__":
    main()
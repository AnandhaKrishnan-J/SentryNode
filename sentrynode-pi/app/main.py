import threading
import logging

from app.sniffer.capture import start_sniffing
from app.flow.aggregator import update_flow, expiration_loop
from app.ml.feature_builder import build_feature_dict
from app.ml.detector import detect
from app.alerts.sender import alert_worker, send_alert
from app.heartbeat import heartbeat_loop


logging.basicConfig(level=logging.INFO)


def process_expired_flow(key, flow):
    try:
        if flow["spkts"] < 3 and flow["dpkts"] < 3:
            return

        if flow["dur"] < 1:
            return

        features = build_feature_dict(key, flow)

        is_anomaly, error, threshold = detect(features)

        if is_anomaly and error > threshold * 1.2:
            logging.warning(f"Anomaly detected | Error: {error:.6f}")
            send_alert(features, error, threshold)

    except Exception as e:
        logging.error(f"Error processing flow: {e}")

def handle_packet(pkt):
    try:
        update_flow(pkt)
    except Exception as e:
        logging.error(f"Error in packet handler: {e}")


def main():
    logging.info("Starting SentryNode Pi Agent...")

    threading.Thread(target=heartbeat_loop, daemon=True).start()

    threading.Thread(target=alert_worker, daemon=True).start()

    threading.Thread(
        target=expiration_loop,
        args=(process_expired_flow,),
        daemon=True
    ).start()

    
    start_sniffing(handle_packet)


if __name__ == "__main__":
    main()
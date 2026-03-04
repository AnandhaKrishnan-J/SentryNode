import threading
import logging

from app.sniffer.capture import start_sniffing
from app.flow.aggregator import update_flow, expire_flows
from app.ml.feature_builder import build_feature_dict
from app.ml.detector import detect
from app.alerts.sender import send_alert
from app.heartbeat import heartbeat_loop


logging.basicConfig(level=logging.INFO)


def handle_packet(pkt):
    try:
        update_flow(pkt)

        expired = expire_flows()

        for key, flow in expired:
            features = build_feature_dict(key, flow)

            is_anomaly, error = detect(features)

            if is_anomaly:
                logging.warning(f"Anomaly detected | Error: {error:.6f}")
                send_alert(features, error)

    except Exception as e:
        logging.error(f"Error in packet handler: {e}")


def main():
    logging.info("Starting SentryNode Pi Agent...")

    threading.Thread(target=heartbeat_loop, daemon=True).start()

    start_sniffing(handle_packet)


if __name__ == "__main__":
    main()
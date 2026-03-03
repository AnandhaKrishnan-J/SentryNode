from app.detection.rules import (
    detect_port_scan,
    detect_large_packet,
    detect_suspicious_port
)

def analyze_packet(packet):

    detectors = [
        detect_port_scan,
        detect_large_packet,
        detect_suspicious_port
    ]

    for detector in detectors:
        alert = detector(packet)
        if alert:
            return alert

    return None


##############################################################################################


from app.detection.rules import (
    detect_port_scan,
    detect_large_packet,
    detect_suspicious_port
)

from app.detection.ml.model_loader import load_model
from app.detection.ml.feature_extractor import extract_features
from app.detection.ml.autoencoder import detect_anomaly

# Load once at startup
ae_model = load_model()

def analyze_packet(packet):

    # Rule-based first
    detectors = [
        detect_port_scan,
        detect_large_packet,
        detect_suspicious_port
    ]

    for detector in detectors:
        alert = detector(packet)
        if alert:
            return alert

    # ML detection
    features = extract_features(packet)
    is_anomaly, score = detect_anomaly(ae_model, features)

    if is_anomaly:
        return {
            "type": "ML_ANOMALY",
            "source_ip": packet["src_ip"],
            "severity": "HIGH",
            "details": f"Reconstruction error: {score}"
        }

    return None
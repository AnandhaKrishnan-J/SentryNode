# app/ml/detector.py

import numpy as np
from app.ml.model_loader import load_artifacts

CATEGORICAL_FEATURES = ["proto", "service", "state"]

NUMERICAL_FEATURES = [
    "dur", "sbytes", "dbytes",
    "spkts", "dpkts",
    "sload", "dload",
    "sjit", "djit",
    "sinpkt", "dinpkt",
    "tcprtt", "synack", "ackdat"
]

SELECTED_FEATURES = CATEGORICAL_FEATURES + NUMERICAL_FEATURES

THRESHOLD =  0.002963997375048398

# Lazy load (better)
_model = None
_scaler = None
_encoders = None
_threshold = None


def get_artifacts():
    global _model, _scaler, _encoders, _threshold

    if _model is None:
        _model, _scaler, _encoders, _threshold = load_artifacts()

    return _model, _scaler, _encoders, _threshold


# Safe encoding
def encode_features(flow_dict, encoders):
    encoded_dict = flow_dict.copy()

    for col in CATEGORICAL_FEATURES:
        value = str(flow_dict.get(col, "unknown"))

        encoder = encoders[col]

        if value in encoder.classes_:
            encoded_value = encoder.transform([value])[0]
        else:
            # safer fallback → assign 0
            encoded_value = 0

        encoded_dict[col] = encoded_value

    return encoded_dict


def prepare_vector(flow_dict, scaler, encoders, model):

    encoded_dict = encode_features(flow_dict, encoders)

    vector = []

    for f in SELECTED_FEATURES:
        value = encoded_dict.get(f, 0.0)
        vector.append(float(value))

    vector = np.array(vector, dtype=float).reshape(1, -1)

    vector_scaled = scaler.transform(vector)

    # safety check
    if vector_scaled.shape[1] != model.input_shape[1]:
        raise ValueError("Feature dimension mismatch with trained model")

    return vector_scaled


def detect(flow_dict):
    try:
        model, scaler, encoders, threshold = get_artifacts()

        # 🔥 FIX: ensure threshold is valid
        if threshold is None:
            print("[WARNING] Threshold is None, using default")
            threshold = 1.0

        vector_scaled = prepare_vector(flow_dict, scaler, encoders, model)

        reconstruction = model.predict(vector_scaled, verbose=0)

        error = float(np.mean(np.square(vector_scaled - reconstruction)))

        is_anomaly = error > threshold

        return is_anomaly, error, threshold

    except Exception as e:
        print(f"[DETECTOR ERROR] {e}")
        return False, 0.0, 1.0
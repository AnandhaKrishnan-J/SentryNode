# app/ml/detector.py

import numpy as np
from app.ml.model_loader import load_artifacts

model, scaler, encoders, threshold = load_artifacts()

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


def encode_features(flow_dict):
    encoded_dict = flow_dict.copy()

    for col in CATEGORICAL_FEATURES:
        value = str(flow_dict[col])

        if value in encoders[col].classes_:
            encoded_value = encoders[col].transform([value])[0]
        else:
            # Fallback to first known class safely
            fallback = encoders[col].classes_[0]
            encoded_value = encoders[col].transform([fallback])[0]

        encoded_dict[col] = encoded_value

    return encoded_dict


def prepare_vector(flow_dict):
    encoded_dict = encode_features(flow_dict)

    vector = [encoded_dict[f] for f in SELECTED_FEATURES]

    vector = np.array(vector, dtype=float).reshape(1, -1)

    vector_scaled = scaler.transform(vector)

    # Safety check
    if vector_scaled.shape[1] != model.input_shape[1]:
        raise ValueError("Feature dimension mismatch with trained model")

    return vector_scaled


def detect(flow_dict):
    vector_scaled = prepare_vector(flow_dict)

    reconstruction = model.predict(vector_scaled, verbose=0)

    error = float(np.mean(np.square(vector_scaled - reconstruction)))

    is_anomaly = error > threshold

    return is_anomaly, error
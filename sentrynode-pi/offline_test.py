import numpy as np
import joblib
from tensorflow.keras.models import load_model

# ===============================
# LOAD ARTIFACTS
# ===============================

model = load_model("models/autoencoder.h5",compile=False)
scaler = joblib.load("models/scaler.pkl")
encoders = joblib.load("models/encoders.pkl")

with open("models/threshold.txt", "r") as f:
    threshold = float(f.read().strip())

print("Model, scaler, encoders loaded.")
print("Threshold:", threshold)

# ===============================
# FEATURE ORDER (CRITICAL)
# ===============================

categorical_features = ["proto", "service", "state"]

numerical_features = [
    "dur", "sbytes", "dbytes",
    "spkts", "dpkts",
    "sload", "dload",
    "sjit", "djit",
    "sinpkt", "dinpkt",
    "tcprtt", "synack", "ackdat"
]

selected_features = categorical_features + numerical_features

# ===============================
# SAFE LABEL ENCODING
# ===============================

def encode(col, value):
    encoder = encoders[col]
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        return -1

# ===============================
# BUILD FEATURE VECTOR
# ===============================

def build_vector(flow):

    vector = []

    for col in categorical_features:
        vector.append(encode(col, flow[col]))

    for col in numerical_features:
        vector.append(flow[col])

    return np.array(vector).reshape(1, -1)

# ===============================
# DETECTION FUNCTION
# ===============================

def detect(flow):

    vector = build_vector(flow)

    if vector.shape[1] != 17:
        raise ValueError("Feature size mismatch! Expected 17.")

    scaled = scaler.transform(vector)

    reconstructed = model.predict(scaled, verbose=0)

    error = np.mean((scaled - reconstructed) ** 2)

    print("Reconstruction error:", error)

    if error > threshold:
        print("🚨 ANOMALY DETECTED")
        return True
    else:
        print("Normal flow")
        return False

# ===============================
# TEST FLOW
# ===============================

sample_flow = {
    "proto": "tcp",
    "service": "http",
    "state": "CON",
    "dur": 0.2,
    "sbytes": 1200,
    "dbytes": 900,
    "spkts": 10,
    "dpkts": 8,
    "sload": 5000,
    "dload": 4000,
    "sjit": 0.1,
    "djit": 0.1,
    "sinpkt": 0.02,
    "dinpkt": 0.02,
    "tcprtt": 0.01,
    "synack": 0.005,
    "ackdat": 0.005,
}

detect(sample_flow)
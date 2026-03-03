import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load once at startup
model = load_model("models/autoencoder.h5", compile=False)
scaler = joblib.load("models/scaler.pkl")
encoders = joblib.load("models/encoders.pkl")

with open("models/threshold.txt", "r") as f:
    # threshold = float(f.read().strip())
    threshold = 0.002

categorical_features = ["proto", "service", "state"]

numerical_features = [
    "dur", "sbytes", "dbytes",
    "spkts", "dpkts",
    "sload", "dload",
    "sjit", "djit",
    "sinpkt", "dinpkt",
    "tcprtt", "synack", "ackdat"
]

def encode(col, value):
    encoder = encoders[col]
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    return -1

def build_vector(flow):
    vector = []

    for col in categorical_features:
        vector.append(encode(col, flow[col]))

    for col in numerical_features:
        vector.append(flow[col])

    return np.array(vector).reshape(1, -1)

def detect(flow):
    vector = build_vector(flow)
    scaled = scaler.transform(vector)
    reconstructed = model.predict(scaled, verbose=0)
    error = np.mean((scaled - reconstructed) ** 2)

    print("threshold" , threshold)

    return error > threshold, error
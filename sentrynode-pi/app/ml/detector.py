# app/ml/detector.py

import numpy as np
import tflite_runtime.interpreter as tflite
from app.ml.model_loader import load_artifacts
from pathlib import Path

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


# ---------------- PATH ---------------- #

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "autoencoder.tflite"


# ---------------- GLOBALS ---------------- #

_scaler = None
_encoders = None
_threshold = None

_interpreter = None
_input_details = None
_output_details = None


# ---------------- LOAD ---------------- #

def get_artifacts():
    global _scaler, _encoders, _threshold
    global _interpreter, _input_details, _output_details

    if _interpreter is None:
        # Load scaler + encoders + threshold
        _scaler, _encoders, _threshold = load_artifacts()

        # Load TFLite model
        _interpreter = tflite.Interpreter(model_path=str(MODEL_PATH))
        _interpreter.allocate_tensors()

        _input_details = _interpreter.get_input_details()
        _output_details = _interpreter.get_output_details()

        print("✅ TFLite model loaded")

    return _scaler, _encoders, _threshold


# ---------------- ENCODING ---------------- #

def encode_features(flow_dict, encoders):
    encoded_dict = flow_dict.copy()

    for col in CATEGORICAL_FEATURES:
        value = str(flow_dict.get(col, "unknown"))

        encoder = encoders[col]

        if value in encoder.classes_:
            encoded_value = encoder.transform([value])[0]
        else:
            encoded_value = 0

        encoded_dict[col] = encoded_value

    return encoded_dict


# ---------------- VECTOR ---------------- #

def prepare_vector(flow_dict, scaler, encoders):
    encoded_dict = encode_features(flow_dict, encoders)

    vector = []

    for f in SELECTED_FEATURES:
        value = encoded_dict.get(f, 0.0)
        vector.append(float(value))

    vector = np.array(vector, dtype=np.float32).reshape(1, -1)

    vector_scaled = scaler.transform(vector)

    # Updated safety check (no TF model now)
    if vector_scaled.shape[1] != len(SELECTED_FEATURES):
        raise ValueError("Feature dimension mismatch")

    return vector_scaled.astype(np.float32)


# ---------------- DETECTION ---------------- #

def detect(flow_dict):
    try:
        scaler, encoders, threshold = get_artifacts()

        #if threshold is None:
        threshold = 0.002963997375048398 * 6

        # ✅ Explicit narrowing for Pylance
        interpreter = _interpreter
        input_details = _input_details
        output_details = _output_details

        if interpreter is None or input_details is None or output_details is None:
            raise RuntimeError("TFLite interpreter not initialized")

        vector = prepare_vector(flow_dict, scaler, encoders)

        interpreter.set_tensor(input_details[0]['index'], vector)
        interpreter.invoke()
        reconstruction = interpreter.get_tensor(output_details[0]['index'])

        error = float(np.mean(np.square(vector - reconstruction)))

        print(f"[Debug] Error = {error:.6f}, {threshold :.6f}")

        is_anomaly = error > threshold

        return is_anomaly, error, threshold

    except Exception as e:
        print(f"[DETECTOR ERROR] {e}")
        return False, 0.0, 1.0
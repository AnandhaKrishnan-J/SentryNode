import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = BASE_DIR / "models"

SCALER_PATH = MODELS_DIR / "scaler.pkl"
ENCODER_PATH = MODELS_DIR / "encoders.pkl"
THRESHOLD_PATH = MODELS_DIR / "threshold.txt"

_cached_artifacts = None


def load_artifacts():
    global _cached_artifacts

    if _cached_artifacts is not None:
        return _cached_artifacts

    scaler = joblib.load(SCALER_PATH)
    encoders = joblib.load(ENCODER_PATH)

    with open(THRESHOLD_PATH, "r") as f:
        threshold = float(f.read().strip())

    _cached_artifacts = (scaler, encoders, threshold)

    return _cached_artifacts
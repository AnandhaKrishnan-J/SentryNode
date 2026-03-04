import joblib
from tensorflow.keras.models import load_model
from pathlib import Path

# Base project directory
BASE_DIR = Path(__file__).resolve().parents[1]

MODELS_DIR = BASE_DIR / "models"

MODEL_PATH = MODELS_DIR / "autoencoder.h5"
SCALER_PATH = MODELS_DIR / "scaler.pkl"
ENCODER_PATH = MODELS_DIR / "encoders.pkl"
THRESHOLD_PATH = MODELS_DIR / "threshold.txt"

_cached_artifacts = None


def load_artifacts():
    global _cached_artifacts

    if _cached_artifacts is not None:
        return _cached_artifacts

    # Validate files exist
    for path in [MODEL_PATH, SCALER_PATH, ENCODER_PATH, THRESHOLD_PATH]:
        if not path.exists():
            raise FileNotFoundError(f"Missing model artifact: {path}")

    model = load_model(str(MODEL_PATH), compile=False)
    scaler = joblib.load(SCALER_PATH)
    encoders = joblib.load(ENCODER_PATH)

    with open(THRESHOLD_PATH, "r") as f:
        threshold = float(f.read().strip())

    _cached_artifacts = (model, scaler, encoders, threshold)

    return _cached_artifacts
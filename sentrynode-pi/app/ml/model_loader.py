import joblib
import os

MODEL_PATH = "app/detection/ml/autoencoder.h5"

def load_model():
    if not os.path.exists(MODEL_PATH, compile=False):
        raise FileNotFoundError("AE model not found")

    model = joblib.load(MODEL_PATH)
    return model
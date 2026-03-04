# app/ml/autoencoder.py

import numpy as np


def detect_anomaly(model, scaled_features, threshold):
    """
    Expects:
        model → loaded autoencoder
        scaled_features → numpy array of shape (1, n_features)
        threshold → float

    Returns:
        (is_anomaly: bool, error: float)
    """

    # Ensure correct shape
    if len(scaled_features.shape) == 1:
        scaled_features = scaled_features.reshape(1, -1)

    reconstructed = model.predict(scaled_features, verbose=0)

    error = np.mean((scaled_features - reconstructed) ** 2)

    is_anomaly = error > threshold

    return is_anomaly, float(error)
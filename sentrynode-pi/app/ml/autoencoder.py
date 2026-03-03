import numpy as np

def detect_anomaly(model, features, threshold=0.01):
    threshold = 0.001
    reconstructed = model.predict(features)
    error = np.mean((features - reconstructed) ** 2)

    if error > threshold:
        return True, error
    print("threshold :",threshold)

    return False, error
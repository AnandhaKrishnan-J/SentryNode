from ml.detector import detect

# -------------------------
# NORMAL SAMPLES
# -------------------------

normal_samples = [
    {
        "proto": "tcp",
        "service": "-",
        "state": "FIN",
        "dur": 0.121478,
        "spkts": 6,
        "dpkts": 4,
        "sbytes": 258,
        "dbytes": 172,
        "sload": 14158.94238,
        "dload": 8495.365234,
        "sinpkt": 24.2956,
        "dinpkt": 8.375,
        "sjit": 30.177547,
        "djit": 11.830604,
        "tcprtt": 0,
        "synack": 0,
        "ackdat": 0,
    }
]

# -------------------------
# ATTACK SAMPLES
# -------------------------

attack_samples = [
    {
        "proto": "tcp",
        "service": "http",
        "state": "FIN",
        "dur": 1.221551,
        "spkts": 10,
        "dpkts": 8,
        "sbytes": 1142,
        "dbytes": 354,
        "sload": 6732.424805,
        "dload": 2030.205933,
        "sinpkt": 135.662667,
        "dinpkt": 164.314,
        "sjit": 7980.979821,
        "djit": 271.56625,
        "tcprtt": 0.131321,
        "synack": 0.071352,
        "ackdat": 0.059969,
    },
    {
        "proto": "udp",
        "service": "dns",
        "state": "INT",
        "dur": 0.000008,
        "spkts": 2,
        "dpkts": 0,
        "sbytes": 114,
        "dbytes": 0,
        "sload": 57000000,
        "dload": 0,
        "sinpkt": 0.008,
        "dinpkt": 0,
        "sjit": 0,
        "djit": 0,
        "tcprtt": 0,
        "synack": 0,
        "ackdat": 0,
    }
]

# -------------------------
# RUN TEST
# -------------------------

print("\n--- NORMAL TESTS ---")
for sample in normal_samples:
    is_anomaly, error = detect(sample)
    print("Error:", error)
    print("Predicted anomaly:", is_anomaly)
    print("-" * 40)

print("\n--- ATTACK TESTS ---")
for sample in attack_samples:
    is_anomaly, error = detect(sample)
    print("Error:", error)
    print("Predicted anomaly:", is_anomaly)
    print("-" * 40)
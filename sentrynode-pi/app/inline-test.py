import pandas as pd
from collections import defaultdict

from app.ml.detector import detect
from app.alerts.sender import send_alert

CSV_PATH = "misc/train_test_network.csv"

df = pd.read_csv(CSV_PATH)

# Sample 100 rows
df = df.sample(n=100, random_state=41)

tp = tn = fp = fn = 0

attack_stats = defaultdict(lambda: {"detected": 0, "total": 0})

print("Running evaluation on 100 random samples...\n")

for i, row in df.iterrows():

    sample = {
        "proto": row["proto"],
        "service": row["service"],
        "state": row["conn_state"],

        "dur": row["duration"],
        "sbytes": row["src_bytes"],
        "dbytes": row["dst_bytes"],

        "spkts": row["src_pkts"],
        "dpkts": row["dst_pkts"],

        "sload": 0,
        "dload": 0,
        "sjit": 0,
        "djit": 0,
        "sinpkt": 0,
        "dinpkt": 0,
        "tcprtt": 0,
        "synack": 0,
        "ackdat": 0
    }

    is_anomaly, error = detect(sample)

    actual = row["label"]
    attack_type = row.get("type", "unknown")

    if actual == 1:
        attack_stats[attack_type]["total"] += 1

    if actual == 1 and is_anomaly:
        tp += 1
        attack_stats[attack_type]["detected"] += 1
    elif actual == 0 and not is_anomaly:
        tn += 1
    elif actual == 0 and is_anomaly:
        fp += 1
    elif actual == 1 and not is_anomaly:
        fn += 1

    if is_anomaly:
        print(f"🚨 Anomaly detected | Row {i} | Error={error:.6f} | Type={attack_type}")

        # Send alert to backend
        send_alert(
            source_ip=row.get("src_ip"),
            destination_ip=row.get("dst_ip"),
            protocol=row.get("proto"),
            error=error,
            description=f"Detected {attack_type} attack"
        )

    else:
        print(f"Normal traffic | Row {i} | Type={attack_type}")

print("\n======================")
print("Evaluation Results")
print("======================")

print(f"TP: {tp}")
print(f"TN: {tn}")
print(f"FP: {fp}")
print(f"FN: {fn}")

precision = tp / (tp + fp) if (tp + fp) else 0
recall = tp / (tp + fn) if (tp + fn) else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
fpr = fp / (fp + tn) if (fp + tn) else 0

print("\nMetrics:")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1:.3f}")
print(f"False Positive Rate: {fpr:.3f}")
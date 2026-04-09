# app/ml/feature_builder.py

def build_feature_dict(key, flow):

    src_ip, dst_ip, src_port, dst_port, proto = key

    dur = flow.get("dur", 0)
    sbytes = flow.get("sbytes", 0)
    dbytes = flow.get("dbytes", 0)
    spkts = flow.get("spkts", 0)
    dpkts = flow.get("dpkts", 0)

    # Avoid division by zero
    dur = max(dur, 1e-6)

    # Basic derived features
    sload = sbytes / dur
    dload = dbytes / dur

    sinpkt = dur / max(spkts, 1)
    dinpkt = dur / max(dpkts, 1)

    # Placeholder features (not implemented yet)
    sjit = 0.0
    djit = 0.0
    tcprtt = 0.0
    synack = 0.0
    ackdat = 0.0

    # Service mapping (simple heuristic)
    if dst_port == 80 or dst_port == 8080:
        service = "http"
    elif dst_port == 443:
        service = "https"
    elif dst_port == 22:
        service = "ssh"
    elif dst_port == 53:
        service = "dns"
    else:
        service = "other"

    # State (basic assumption)
    state = "CON"

    feature_dict = {
        # Metadata (useful for alerts)
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port,
        "dst_port": dst_port,

        # ML features
        "proto": proto,
        "service": service,
        "state": state,

        "dur": dur,
        "sbytes": sbytes,
        "dbytes": dbytes,
        "spkts": spkts,
        "dpkts": dpkts,

        "sload": sload,
        "dload": dload,

        "sinpkt": sinpkt,
        "dinpkt": dinpkt,

        "sjit": sjit,
        "djit": djit,

        "tcprtt": tcprtt,
        "synack": synack,
        "ackdat": ackdat,
    }

    return feature_dict
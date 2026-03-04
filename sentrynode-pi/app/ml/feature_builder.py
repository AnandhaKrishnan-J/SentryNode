def infer_service(port):
    if port == 80:
        return "http"
    elif port == 443:
        return "http"
    elif port == 53:
        return "dns"
    elif port == 21:
        return "ftp"
    elif port == 20:
        return "ftp-data"
    elif port == 22:
        return "ssh"
    else:
        return "-"


def build_feature_dict(key, flow):

    src_ip, dst_ip, src_port, dst_port, proto = key

    duration = flow["dur"]
    sbytes = flow["sbytes"]
    spkts = flow["spkts"]

    # Stabilize calculations
    if duration > 0.001:
        sload = sbytes / duration
    else:
        sload = 0

    sinpkt = duration / spkts if spkts > 0 else 0

    return {
        "proto": proto,
        "service": infer_service(dst_port),
        "state": "CON",

        "dur": duration,
        "sbytes": sbytes,
        "dbytes": 0,

        "spkts": spkts,
        "dpkts": 0,

        "sload": sload,
        "dload": 0,

        "sjit": 0,
        "djit": 0,

        "sinpkt": sinpkt,
        "dinpkt": 0,

        "tcprtt": 0,
        "synack": 0,
        "ackdat": 0,
    }
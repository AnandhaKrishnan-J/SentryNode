import time

FLOW_TIMEOUT = 10
flows = {}


def get_key(pkt):
    return (
        pkt["src_ip"],
        pkt["dst_ip"],
        pkt["src_port"],
        pkt["dst_port"],
        pkt["proto"]
    )


def get_reverse_key(pkt):
    return (
        pkt["dst_ip"],
        pkt["src_ip"],
        pkt["dst_port"],
        pkt["src_port"],
        pkt["proto"]
    )


def update_flow(pkt):
    key = get_key(pkt)
    rev_key = get_reverse_key(pkt)

    now = time.time()

    # Check if reverse flow exists
    if rev_key in flows:
        flow = flows[rev_key]

        flow["last_seen"] = now
        flow["dbytes"] += pkt["size"]
        flow["dpkts"] += 1

    else:
        if key not in flows:
            flows[key] = {
                "start_time": now,
                "last_seen": now,
                "sbytes": 0,
                "spkts": 0,
                "dbytes": 0,
                "dpkts": 0,
            }

        flow = flows[key]

        flow["last_seen"] = now
        flow["sbytes"] += pkt["size"]
        flow["spkts"] += 1


def expire_flows():
    now = time.time()
    expired = []

    for key in list(flows.keys()):
        flow = flows[key]

        if now - flow["last_seen"] > FLOW_TIMEOUT:

            flow["dur"] = flow["last_seen"] - flow["start_time"]

            # Avoid division issues later
            flow["dur"] = max(flow["dur"], 1e-6)

            expired.append((key, flow))
            del flows[key]

    return expired
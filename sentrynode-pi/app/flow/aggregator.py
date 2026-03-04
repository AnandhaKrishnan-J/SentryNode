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


def update_flow(pkt):
    key = get_key(pkt)

    now = time.time()  # use consistent clock

    if key not in flows:
        flows[key] = {
            "start_time": now,
            "last_seen": now,
            "sbytes": 0,
            "spkts": 0,
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
            # Compute duration here
            flow["dur"] = flow["last_seen"] - flow["start_time"]

            expired.append((key, flow))
            del flows[key]

    return expired
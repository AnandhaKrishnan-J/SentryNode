from scapy.layers.inet import IP, TCP, UDP
import time

def parse_packet(pkt):

    if IP not in pkt:
        return None

    protocol = None
    src_port = 0
    dst_port = 0

    if TCP in pkt:
        protocol = "tcp"
        src_port = pkt[TCP].sport
        dst_port = pkt[TCP].dport

    elif UDP in pkt:
        protocol = "udp"
        src_port = pkt[UDP].sport
        dst_port = pkt[UDP].dport
    else:
        protocol = "other"

    return {
        "timestamp": time.time(),
        "src_ip": pkt[IP].src,
        "dst_ip": pkt[IP].dst,
        "src_port": src_port,
        "dst_port": dst_port,
        "proto": protocol,
        "size": len(pkt)
    }
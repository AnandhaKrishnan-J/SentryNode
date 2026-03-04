from scapy.layers.inet import IP, TCP, UDP
import time


def parse_packet(pkt):
    try:
        if IP not in pkt:
            return None

        if TCP in pkt:
            protocol = "tcp"
            src_port = pkt[TCP].sport
            dst_port = pkt[TCP].dport

        elif UDP in pkt:
            protocol = "udp"
            src_port = pkt[UDP].sport
            dst_port = pkt[UDP].dport

        else:
            return None  # ignore unsupported protocols

        return {
            "timestamp": time.time(),
            "src_ip": pkt[IP].src,
            "dst_ip": pkt[IP].dst,
            "src_port": src_port,
            "dst_port": dst_port,
            "proto": protocol,
            "size": len(pkt)
        }

    except Exception:
        return None
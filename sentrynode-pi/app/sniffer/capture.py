from scapy.all import sniff, get_if_list
from app.sniffer.parser import parse_packet
from app.config import settings


def get_interface():
    # If user configured interface → use it
    if settings.INTERFACE:
        return settings.INTERFACE

    # Auto-detect fallback
    interfaces = get_if_list()

    for iface in interfaces:
        if "wlan" in iface:
            return iface
        if "eth" in iface:
            return iface

    raise RuntimeError("No suitable network interface found")


def start_sniffing(packet_handler):

    def handle(pkt):
        parsed = parse_packet(pkt)
        if parsed:
            packet_handler(parsed)

    try:
        iface = get_interface()
        print(f"📡 Sniffing on interface: {iface}")

        sniff(
            iface=iface,
            prn=handle,
            store=False,
            filter="tcp or udp",
            promisc=True
        )

    except PermissionError:
        print("❌ Permission denied. Run with sudo.")
    except Exception as e:
        print(f"Sniffer error: {e}")
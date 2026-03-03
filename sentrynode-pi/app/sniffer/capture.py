from scapy.all import sniff
from app.sniffer.parser import parse_packet
from app.config import settings

def start_sniffing(packet_handler):

    def handle(pkt):
        parsed = parse_packet(pkt)
        if parsed:
            packet_handler(parsed)

    sniff(iface=settings.INTERFACE, prn=handle, store=False)
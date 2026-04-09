import requests
from requests.adapters import HTTPAdapter


ETH0_IP = "192.168.0.2"  # Pi IP


class SourceIPAdapter(HTTPAdapter):
    def __init__(self, source_ip, **kwargs):
        self.source_ip = source_ip
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs["source_address"] = (self.source_ip, 0)
        return super().init_poolmanager(*args, **kwargs)


session = requests.Session()
session.mount("http://", SourceIPAdapter(ETH0_IP))
session.mount("https://", SourceIPAdapter(ETH0_IP))
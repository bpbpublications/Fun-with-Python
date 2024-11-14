import coloredlogs
import os
import logging
import time
import requests
from dnslib import QTYPE
from dnslib.proxy import ProxyResolver as BaseProxyResolver
from dnslib.server import DNSServer


def fetch_dns_blacklist():
    url = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/light.txt"
    response = requests.get(url)
    return response.text.split("\n")


def load_local():
    local_file = "blacklist.txt"
    if os.path.exists(local_file):
        with open(local_file, "r") as f:
            return f.read().split("\n")
    return []


GLOBAL_BLACKLIST = fetch_dns_blacklist()
LOCAL_BLACKLIST = load_local()


def is_name_valid(site_name):
    return site_name not in GLOBAL_BLACKLIST and site_name not in LOCAL_BLACKLIST


class ProxyResolver(BaseProxyResolver):
    def __init__(self, upstream: str):
        super().__init__(address=upstream, port=53, timeout=10)

    def resolve(self, request, handler):
        type_name = QTYPE[request.q.qtype]
        q_name = str(request.q.get_qname()).strip(".")
        logging.info(f"Query type: {type_name}, name: {q_name}")
        if is_name_valid(q_name):
            logging.info("Query not on the blacklist")
            return super().resolve(request, handler)


class DNSService:
    def __init__(self, port: int, upstream: str):
        self.port: int = DEFAULT_PORT if port is None else int(port)
        self.upstream: str | None = upstream
        self.udp_server: DNSServer | None = None
        self.tcp_server: DNSServer | None = None

    def start(self):
        logging.info(f"Listen on port {self.port}, upstream DNS server {self.upstream}")
        resolver = ProxyResolver(self.upstream)

        self.udp_server = DNSServer(resolver, port=self.port)
        self.tcp_server = DNSServer(resolver, port=self.port, tcp=True)
        self.tcp_server.start_thread()
        self.udp_server.start_thread()

    def stop(self):
        self.stop_udp()

    def stop_udp(self):
        self.udp_server.stop()
        self.udp_server.server.server_close()

    def stop_tcp(self):
        self.tcp_server.stop()
        self.tcp_server.server.server_close()

    @property
    def is_running(self):
        if self.udp_server and self.tcp_server:
            return self.udp_server.isAlive() and self.tcp_server.isAlive()
        return False


if __name__ == "__main__":
    coloredlogs.install(level=logging.DEBUG)
    s = DNSService(8953, "1.1.1.1")
    s.start()
    while s.is_running:
        time.sleep(0.1)
    # print(fetch_dns_blacklist())

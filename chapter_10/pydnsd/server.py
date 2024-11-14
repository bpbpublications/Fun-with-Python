import coloredlogs
import logging
import time
from dnslib import QTYPE
from dnslib.proxy import ProxyResolver as BaseProxyResolver
from dnslib.server import DNSServer


class ProxyResolver(BaseProxyResolver):
    def __init__(self, upstream: str):
        super().__init__(address=upstream, port=53, timeout=10)

    def resolve(self, request, handler):
        type_name = QTYPE[request.q.qtype]
        print(dir(request.q))
        logging.info("no local zone found, proxying %s[%s]", request.q.qname, type_name)
        return super().resolve(request, handler)


class DNSService:
    def __init__(self, port: int, upstream: str):
        self.port: int = DEFAULT_PORT if port is None else int(port)
        self.upstream: str | None = upstream
        self.udp_server: DNSServer | None = None
        self.tcp_server: DNSServer | None = None

    def start(self):
        logging.info('starting DNS server on port %d, upstream DNS server "%s"', self.port, self.upstream)
        resolver = ProxyResolver(self.upstream)

        self.udp_server = DNSServer(resolver, port=self.port)
        self.tcp_server = DNSServer(resolver, port=self.port, tcp=True)
        self.udp_server.start_thread()
        self.tcp_server.start_thread()

    def stop(self):
        self.udp_server.stop()
        self.udp_server.server.server_close()
        self.tcp_server.stop()
        self.tcp_server.server.server_close()

    @property
    def is_running(self):
        return (self.udp_server and self.udp_server.isAlive()) or (self.tcp_server and self.tcp_server.isAlive())


if __name__ == "__main__":
    coloredlogs.install(level=logging.DEBUG)
    s = DNSService(8953, "1.1.1.1")
    s.start()
    while s.is_running:
        time.sleep(0.1)

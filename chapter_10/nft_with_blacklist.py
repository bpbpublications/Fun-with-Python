from pyroute2.netlink.nfnetlink.nftsocket import NFPROTO_IPV4
from pyroute2.nftables.main import NFTables
from pyroute2.nftables.main import NFTSetElem
from threading import Thread


class IPUdpater(Thread):
    def __init__(self, nft, filter_set):
        super().__init__()
        self, nft = nft
        self.filter_set = filter_set
        self.running = True
        self.filter_elements = []

    def load_blacklist_ips():
        if os.path.exists("blacklist_ips.txt"):
            with open("blacklist_ips.txt", "r") as f:
                return f.read().split("\n")
        return []

    def run(self):
        while self.running:
            for ip in self.load_blacklist_ips():
                if ip not in self.filter_elements:
                    print(f"Addding ip {ip} to filtered list {self.filter_set}")
                    self.add_element(ip)
            time.sleep(10)
            self.filter_elements = []

    def add_element(self, ip_address):
        nft.set_elems(
            "add",
            set=self.filter_set,
            elements={NFTSetElem(value=ip_address, timeout=10000)},
        )

    def stop(self):
        self.running = False


def main():
    with NFTables(nfgen_family=NFPROTO_IPV4) as nft:
        nft.table("add", name="filter_1")
        my_set = nft.sets(
            "add", table="filter", name="test", key_type="ipv4_addr", comment="my test fw filter", timeout=0
        )
        print("Starting IPs analyzer")
        ip_udpater = IPUdpater(nft, my_set)
        ip_udpater.start()


main()

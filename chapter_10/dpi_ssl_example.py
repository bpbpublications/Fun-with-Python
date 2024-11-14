import os
from nfstream import NFStreamer


def load_blacklist_ips():
    if os.path.exists("blacklist_ips.txt"):
        with open("blacklist_ips.txt", "r") as f:
            return f.read().split("\n")
    return []


def load_blacklist_domains():
    if os.path.exists("blacklist.txt"):
        with open("blacklist.txt", "r") as f:
            return f.read().split("\n")
    return []


def dump_ips():
    with open("blacklist_ips.txt", "w") as f:
        return f.write("\n".join(BLACKLIST_IPS))


BLACKLIST = load_blacklist_domains()
BLACKLIST_IPS = load_blacklist_ips()


def filter_blacklist(frame):
    if frame.requested_server_name.strip() in BLACKLIST and frame.dst_ip not in BLACKLIST_IPS:
        print(f"blacklisted {frame.requested_server_name}")
        BLACKLIST_IPS.append(frame.dst_ip)
        dump_ips()


def main():
    ff = "tcp port 80 or 443"
    my_streamer = NFStreamer(
        source="eno1",
        statistical_analysis=False,
        idle_timeout=1,
        bpf_filter=ff,
    )
    print("start printing")
    for flow in my_streamer:
        filter_blacklist(flow)


main()

import click
import random
import socket
import time
from utils import random_mac_address, get_client_mac_address, get_client_ip

arp_table = {}


def start_routing(in_port, out_port):
    router_mac_addr = random_mac_address().encode()
    router_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    router_in.bind(("localhost", in_port))
    router_in.listen(3)

    router_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    router_out.connect(("localhost", out_port))

    client_id = 1
    while len(arp_table.keys()) < 3:
        client, address = router_in.accept()
        client_ip = get_client_ip(client_id)
        click.echo(f"Client connected: {client_ip}")
        arp_table[client_ip.encode()] = {"client": client, "mac_addr": get_client_mac_address(client_id).encode()}
        client_id += 1
    click.echo(f"ARP table: {arp_table}")
    while True:
        pkt = b""
        while True:
            single_byte = router_out.recv(1)
            if single_byte == b"\n":
                break
            pkt += single_byte

        src_mac = pkt[0:17]
        dst_mac = pkt[17:34]
        src_ip = pkt[34 : 34 + 12 + 3]  # example 180.101.231.245
        dst_ip = pkt[34 + len(src_ip) : 59]
        message = pkt[59:]
        click.echo(f"Source IP: {src_ip}, destination: {dst_ip}")
        click.echo(f"Message: {message}")

        ethernet_header = router_mac_addr + arp_table[dst_ip]["mac_addr"]
        ip_header = src_ip + dst_ip
        out_pkt = ethernet_header + ip_header + message

        dst_socket = arp_table[dst_ip]["client"]
        dst_socket.send(out_pkt)


@click.command()
@click.option("--router-port", default=9340, type=int, help="Incoming router port")
@click.option("--dst-port", default=8080, type=int, help="Destination server port")
def main(dst_port, router_port):
    start_routing(router_port, dst_port)


if __name__ == "__main__":
    main()

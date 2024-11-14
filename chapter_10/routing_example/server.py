import click
import random
import socket
import time
from utils import random_mac_address, random_client_ip, get_client_ip, get_client_mac_address


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8080))
    server.listen(2)
    server_ip = random_client_ip()
    server_mac_addr = random_mac_address()

    click.echo("waiting for router connection...")
    while True:
        routerConnection, address = server.accept()
        if routerConnection != None:
            click.echo("Router Connected Succesfully....!")
            break
    click.echo("Start sending messages...")
    while True:
        for item in range(1, 4):
            message = f"message {item} - pkt {random.randint(0, 254)}"
            destination_ip = get_client_ip(item)
            source_ip = server_ip
            ip_addr_header = source_ip + destination_ip
            source_mac = server_mac_addr
            destination_mac = get_client_mac_address(0)
            eth_header = source_mac + destination_mac
            packet = eth_header + ip_addr_header + message + "\n"
            click.echo(f"send message {item}, packet {packet}")
            routerConnection.send(packet.encode())
        time.sleep(1)


if __name__ == "__main__":
    main()

import click
import random
import socket
import time
from utils import get_client_mac_address, get_client_ip

ROUTER_HOST = "localhost"
ROUTER_PORT = 9340


@click.command()
@click.option("--client-id", type=int, help="client ID (number)", required=True)
def main(client_id):
    mac_addr = get_client_mac_address(client_id)
    ip_addr = get_client_ip(client_id)

    click.echo(f"Using MAC address: {mac_addr}")
    click.echo(f"Using IP address: {ip_addr}")

    router = (ROUTER_HOST, ROUTER_PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # time.sleep(random.randint(1, 3))
    client.connect(router)

    click.echo("Receive data packet")

    while True and client:
        received_message = client.recv(1024)
        received_message = received_message.decode("utf-8")
        source_mac = received_message[0:17]
        destination_mac = received_message[17:34]
        source_ip = received_message[34:45]
        destination_ip = received_message[45:56]
        message = received_message[56:]
        print("\nMessage: " + message)
        time.sleep(1)


if __name__ == "__main__":
    main()

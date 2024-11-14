import socket
from pprint import pprint

HOST = "wikipedia.org"
PORTS = [443, 80, 25]

connection_results = {}

for port in PORTS:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        status = s.connect_ex((HOST, port))
        connection_results[port] = True if status == 0 else False

pprint(connection_results)

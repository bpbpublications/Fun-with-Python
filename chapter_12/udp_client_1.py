import socket

HOST = "localhost"
PORT = 62222

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(10)
    s.connect((HOST, PORT))
    s.settimeout(None)
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data}")

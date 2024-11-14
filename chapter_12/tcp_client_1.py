import socket

HOST = "localhost"
PORT = 62222

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(10)
    status = s.connect_ex((HOST, PORT))
    if status == 0:
        s.settimeout(None)
        s.sendall(b"ping")
        data = s.recv(1024)
        print(data)
    else:
        print(f"Connection error code {status}")

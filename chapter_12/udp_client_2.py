import socket

HOST = "localhost"
PORT = 62222

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(10)
    try:
        status = s.connect_ex((HOST, PORT))
        if status == 0:
            s.settimeout(None)
            s.sendall(b"ping")
            data = s.recv(1024)
            print(data)
    except ConnectionRefusedError:
        status = -1
    if status != 0:
        print(f"Connection error code {status}")

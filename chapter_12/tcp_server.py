import socket

HOST = "localhost"
PORT = 62222

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by client: {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

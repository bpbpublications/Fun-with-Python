import socketserver

HOST = "localhost"
PORT = 62222


class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print(f"Received: {data}")
        socket.sendto(data.upper(), self.client_address)


if __name__ == "__main__":
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()

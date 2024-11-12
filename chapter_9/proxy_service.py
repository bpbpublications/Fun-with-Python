import socketserver
from urllib.request import urlopen
from http.server import SimpleHTTPRequestHandler

PORT = 9097
HOST = "localhost"


class MyProxy(SimpleHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        print(f"Opening URL: {url}")
        self.send_response(200)
        self.end_headers()
        self.copyfile(urlopen(url), self.wfile)


with socketserver.TCPServer((HOST, PORT), MyProxy) as server:
    print(f"Now serving at {PORT}")
    server.serve_forever()

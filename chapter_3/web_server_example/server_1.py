from twisted.web import server, resource
from twisted.internet import reactor, defer


class MyServer(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        uri_path = request.uri.decode('utf-8')
        print(f"Received request for '{uri_path}'")
        return f"Hello, world! {uri_path}".encode('utf8')

service = server.Site(MyServer())
reactor.listenTCP(8083, service)
reactor.run()

from urllib import parse
from twisted.web import server, resource
from twisted.internet import reactor

"""
Web server with support for resource path and query string
"""

class MyServer(resource.Resource):
    isLeaf = True

    def main_view(self):
        return "main view"

    def hello_view(self, **kwargs):
        if kwargs and kwargs.get('a') and kwargs.get('b'):
            total = int(kwargs['a']) + int(kwargs['b'])
            return f"Total sum: {total}"
        return 'hello to you too'

    def convert_query_string(self, resource):
        """Convert query strin to Python dictionary"""
        parsed_data = parse.urlparse(resource).query
        return dict(parse.parse_qsl(parsed_data, keep_blank_values=True))

    def path_finder(self, request):
        resource = request.uri.decode('utf-8')
        query_kwargs = self.convert_query_string(resource)
        parsed_data = parse.urlparse(resource)
        resource_path = parsed_data.path
        result = f"Sorry do not know you {resource}"

        if resource_path == '/':
            result = self.main_view()
        elif resource_path == '/hello':
            result = self.hello_view(**query_kwargs)

        return result

    def render_GET(self, request):
        output = self.path_finder(request)
        if output:
            return output.encode('utf8')
        return b"Something went wrong"

if __name__ == '__main__':
    service = server.Site(MyServer())
    reactor.listenTCP(8083, service)
    reactor.run()

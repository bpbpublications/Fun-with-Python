from twisted.internet import reactor
from twisted.web import server

from server_2 import MyServer


class MyServer2(MyServer):

    def hello_view(self, **kwargs):
        if kwargs and kwargs.get('a') and kwargs.get('b'):
            try:
                total = int(kwargs['a']) + int(kwargs['b'])
                return f"Total sum: {total}"
            except ValueError:
                return "One of the arguments is not a number"
        return 'hello to you too'


def start_seervice():
    service = server.Site(MyServer2())
    reactor.listenTCP(8083, service)
    reactor.run()


if __name__ == '__main__':
    start_seervice()
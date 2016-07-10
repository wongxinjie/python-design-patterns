# coding: utf-8
# Factory is not a design pattern by itself; rather, it's a concept that serves
# as a basis for # several design patterns such as Factory Method and
# Abstract Factory.


class HTTPConnection(object):
    def connect(self):
        print "connect via http"


class FTPConnection(object):
    def connect(self):
        print "connect via ftp"


class SimpleFactory(object):
    @staticmethod
    def build_connetion(protocol):
        if protocol == "http":
            return HTTPConnection()
        elif protocol == "ftp":
            return FTPConnection()


if __name__ == "__main__":
    protocol = "ftp"
    conn = SimpleFactory.build_connetion(protocol)
    conn.connect()

# coding: utf-8
# Advantages of using the Abstract Factory pattern
# The main advantages of using the Abstract Factory pattern are as follows:
#     • It simplifies the replacement of product families
#     • It ensures the compatibility of the products in the product's family
#     • It isolates the concrete classes from the client
import abc
import urllib2

from BeautifulSoup import BeautifulSoup as BS


class AbstractFactory(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, is_secure):
        self.is_secure = is_secure

    @abs.abstractmethod
    def create_protocol(self):
        pass

    @abc.abstractmethod
    def create_port(self):
        pass

    @abc.abstractmethod
    def parse(self):
        pass


class HTTPFactory(AbstractFactory):

    def create_protocol(self):
        if self.is_secure:
            return "https"
        return "http"

    def create_port(self):
        if self.is_secure:
            return HTTPSecurePort()
        return HTTPPort()

    def create_parse(self):
        return HTTPParser()


class FTPFactory(AbstractFactory):

    def create_protocol(self):
        return 'ftp'

    def create_port(self):
        return FTPPort()

    def create_parser(self):
        return FTPParser()


class Port(object):
    __metaclass__ = abc.ABCMeta

    @abs.abstractmethod
    def __str__(self):
        pass


class HTTPPort(Port):
    def __str__(self):
        return '80'


class HTTPSecurePort(Port):
    def __str__(self):
        return '443'


class FTPPort(Port):
    def __str__(self):
        return '80'


class Parser(object):

    @abc.abstractmethod
    def __call__(self, content):
        pass


class HTTPParser(Parser):

    def __call__(self, content):
        filenames = []
        bs = BS(content)
        links = bs.table.findAll('a')
        for link in links:
            filenames.append(link['href'])
        return '\n'.join(filenames)


class FTPParser(Parser):

    def __call__(self, content):
        lines = content.split('\n')
        filenames = []
        for line in lines:
            parts = line.split(None, 8)
            if len(parts) == 9:
                filenames.append(parts[-1])
        return '\n'.join(filenames)


class Connector(object):

    def __init__(self, factory):
        self.protocol = factory.create_protocol()
        self.port = factory.create_port()
        self.parse = factory.create_parse()

    def read(self, host, path):
        url = "{}://{}:{}{}".format(
            self.protocol, host, self.port, path)
        print "Connect to ", url
        return urllib2.urlopen(url, timeout=2).read()

    @abc.abstractmethod
    def parse(self):
        pass


if __name__ == "__main__":
    doamin = "ftp.freebsd.org"
    path = "/pub/FreeBSD"

    factory = HTTPFactory()
    is_secure = False

    connector = Connector(factory)
    try:
        content = connector.read(doamin, path)
    except Exception as err:
        print err
    else:
        print connector.parse(content)

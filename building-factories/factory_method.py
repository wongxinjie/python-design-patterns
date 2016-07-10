# coding: utf-8
# Advantages of using the Factory Method pattern
# The main advantages of using the Factory Method pattern are:
#     • It makes code more universal, not being tied to concrete classes
#     ( ConcreteProduct ) but to interfaces ( Product ) providing low coupling.
#     It separates interfaces from their implementations.
#     • It decouples the code that creates objects from the code that uses
#     them,
#     reducing the complexity of maintenance. To add a new class, you need to
#     add an additional else-if clause.
import abc
import urllib2

from BeautifulSoup import BeautifulSoup as BS


class Connector(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, is_secure):
        self.is_secure = is_secure
        self.port = self.port_factory_method()
        self.protocol = self.protocol_factory_method()

    @abc.abstractmethod
    def parse(self):
        pass

    def read(self, host, path):
        url = "{}://{}:{}{}".format(
            self.protocol, host, self.port, path)
        return urllib2.urlopen(url, timeout=2).read()

    @abc.abstractmethod
    def protocol_factory_method(self):
        pass

    @abc.abstractmethod
    def port_factory_method(self):
        pass


class HTTPConnector(Connector):

    def protocol_factory_method(self):
        if self.is_secure:
            return 'https'
        return 'http'

    def port_factory_method(self):
        if self.is_secure:
            return HTTPSecurePort()
        return HTTPPort()

    def parse(self, content):
        filenames = []
        bs = BS(content)
        links = bs.table.findAll('a')
        for link in links:
            filenames.append(link['href'])
        return '\n'.join(filenames)


class FTPConnector(Connector):

    def protocol_factory_method(self):
        return 'ftp'

    def port_factory_method(self):
        return FTPPort()

    def parse(self, content):
        lines = content.split('\n')
        filenames = []
        for line in lines:
            parts = line.split(None, 8)
            if len(parts) == 9:
                filenames.append(parts[-1])
        return '\n'.join(filenames)


class Port(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
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


if __name__ == "__main__":
    domain = 'ftp.freebsd.org'
    path = '/pub/FreeBSD'

    protocol = 0
    is_secure = False

    if protocol == 0:
        connector = HTTPConnector(is_secure)
    else:
        connector = FTPConnector(is_secure)

    try:
        content = connector.read(domain, path)
    except urllib2.URLError as err:
        print err
    else:
        print connector.parse(content)

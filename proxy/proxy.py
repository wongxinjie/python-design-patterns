# coding: utf-8
import random
from abc import ABCMeta, abstractmethod


class AbstractSubject(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def sort(self, reverse=False):
        pass


class RealObject(object):

    def __init__(self):
        self.digits = [random.random() for _ in range(10000)]

    def sort(self, reverse=False):
        self.digits.sort()

        if reverse:
            self.digits.reverse()


class Proxy(AbstractSubject):

    reference_count = 0

    def __init__(self):
        if not getattr(self.__class__, 'cached_object', None):
            self.__class__.cached_object = RealObject()
            print 'Create new object'
        else:
            print 'Using cached object'
        self.__class__.reference_count += 1
        print 'Count of reference = ', self.__class__.reference_count

    def sort(self, reverse=False):
        print 'Called sort method with args:'
        print locals().items()
        self.__class__.cached_object.sort(reverse=reverse)

    def __del__(self):
        self.__class__.reference_count -= 1
        if self.__class__.reference_count == 0:
            print 'Delete cached object...'
            del self.__class__.cached_object

        print ("Delete object. Count of objects = ",
               self.__class__.reference_count)


if __name__ == "__main__":
    proxy1 = Proxy()
    print '-' * 80
    proxy2 = Proxy()
    print '-' * 80
    proxy3 = Proxy()
    print '-' * 80

    proxy1.sort(reverse=True)
    print '-' * 80

    print 'Deleting proxy2'
    del proxy2
    print '-' * 80

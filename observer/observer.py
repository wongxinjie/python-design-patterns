# coding: utf-8
import abc
import time
from datetime import datetime


class Subject(object):

    def __init__(self):
        self.observers = []
        self.current_time = None

    def register_observer(self, observer):
        if observer in self.observers:
            print observer, ' already in subscribed observers'
        else:
            self.observers.append(observer)

    def unregister_observer(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            print "No subject observer in subject"

    def notity_observers(self):
        self.current_time = time.time()
        for observer in self.observers:
            observer.notify(self.current_time)


class Observer(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def notify(self, unix_timestamp):
        pass


class USATimeObserver(Observer):

    def __init__(self, name):
        self.name = name

    def notify(self, unix_timestamp):
        ts = datetime.fromtimestamp(
            int(unix_timestamp)).strftime("%Y-%m-%d %I:%M:%S%p")
        print "Observer ", self.name, "says: ", ts


class EUTimeObserver(Observer):

    def __init__(self, name):
        self.name = name

    def notify(self, unix_timestamp):
        ts = datetime.fromtimestamp(
            int(unix_timestamp)).strftime("%Y-%m-%d %H:%M:%S")
        print "Observer ", self.name, "says: ", ts


if __name__ == "__main__":
    subject = Subject()

    observer1 = USATimeObserver("usa_time_observer")
    subject.register_observer(observer1)
    subject.notity_observers()

    time.sleep(2)
    observer2 = EUTimeObserver('eu_time_observer')
    subject.register_observer(observer2)
    subject.notity_observers()

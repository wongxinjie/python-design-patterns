# coding: utf-8
# Borg is also known as monostate. In the borg pattern,
# all of the instances are different, but they share the same state.


class Borg(object):
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        instance = super(Borg, cls).__new__(cls, *args, **kwargs)
        instance.__dict__ = cls._shared_state
        return instance


class Child(Borg):
    pass

borg = Borg()
another_borg = Borg()
print borg is another_borg

child = Child()
print child is borg

borg.var = 'A'
print child.var

# If you want to have a class that is a descendant of
# the Borg class but has a different state,
# you can reset shared_state as follows:


class AnotherChild(Borg):
    _shared_state = {}

another_child = AnotherChild()
print another_child.var
# AttributeError: 'AnotherChild' object has no attribute 'var'

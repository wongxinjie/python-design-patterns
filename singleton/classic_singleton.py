# coding: utf-8
class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


singleton = Singleton()
another_sinngleton = Singleton()

print(singleton is another_sinngleton)
singleton.var = "A"
print(another_sinngleton.var)


# Oops
class Child(Singleton):
    pass

# If some class is a successor of Singleton, all successor's instances
# should also be the instances of Singleton, thus sharing its states.
# But this doesn't work, as illustrated in the following code:

child = Child()
print(child is singleton)
print(child.var)

# Well, this works on my thinkpad. I use python2.7/python3.5, Ubuntu.

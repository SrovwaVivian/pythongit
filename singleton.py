def singleton(cls, *args, **kw):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance

@singleton
class MyClass:
...


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton,cls).__new__(cls, *args, **kw)
        return cls._instance

class MyClass(Singleton):
    def __init__(self,s):
            self.s = s
a = MyClass('apple')
b = MyClass('banana')

def singleton(cls, *args, **kw):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance

@singleton
class MyClass:
    pass


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton,cls).__new__(cls, *args, **kw)
        return cls._instance

class MyClass2(Singleton):
    def __init__(self,s):
            self.s = s
a = MyClass2('apple')
b = MyClass2('banana')

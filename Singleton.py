class Singleton(type):
    def __init__(cls,name,bases,attrs):
        super(Singleton,cls).__init__(name,bases,attrs)
        cls.instance = None
    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = super(Singleton,cls).__call__(*args,**kw)
        return cls.instance

class Myclass(object):
    __metaclass__ = Singleton

print (Myclass())
print (Myclass())

def Singleton2(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            return instances[cls] = cls()
    return getinstance
@Singleton2
class Myclass2():
    

#coding:utf-8
import random
import functools
a= [random.randint(0,10) for i in range(10)]
print (a)
print (list(set(a)))


print ({}.fromkeys(a).keys())
a.sort()
print([x for i,x in enumerate(a) if not i or x != a[i-1]])

print (functools.reduce(lambda x,y:x if y in x else x + [y],[[],]+a))
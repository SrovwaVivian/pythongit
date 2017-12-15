# coding:utf-8
"""
stack.py
"""

class Stack(object):
    def __init__(self,size = 20):
        self.stack = []
        self.size  = size
        self.top = -1
    @property
    def empty(self):
        self.stack = []
        self.top = -1

    def size(self):
        return self.size
    
    def setsize(self,size):
        self.size = size
    
    def push(self,element):
        if self.isfull:
            print ('StackOverFlow')
        else:
            self.stack.append(element)
            self.top += 1

    def pop(self):
        if self.isempty:
            print ("StackUnderFlow")
        else:
            element = self.stack[-1]
            del self.stack[-1]
            self.top -= 1
        return element
    @property
    def isfull(self):
        if self.top == self.size -1:
            return True
        return False
    @property
    def isempty(self):
        if self.top == -1:
            return True
        return False
    

    def top(self):
        return self.top
    @property
    def show(self):
        return self.stack

if __name__ == '__main__':
    stack = Stack()



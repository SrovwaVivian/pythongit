"""
queue.py
"""

class Queue(object):
    def __init__(self,size = 20):
        self.size = size
        self.start = 0
        self.queue = []

    def put(self,element):
        if self.start < self.size:
            self.queue.append(element)
            self.start += 1
        else:
            print('Full')
    
    def get(self):
        if self.start != 0:
            element = self.queue[0]
            del self.queue[0]
            self.start -= 1
        else:
            print('empty')
    
    def start(self):
        return self.start

    def empty(self):
        self.queue = []
        self.start =0



if __name__ == '__main__':
    queue = Queue()
    queue.put(2)
    print(queue.start)
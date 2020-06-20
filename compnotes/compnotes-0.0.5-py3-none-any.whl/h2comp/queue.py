class Queue():
    def __init__(self, size):
        self.head = -1
        self.tail = 0
        self.size = size
        self.arr = [None] * size
    
    def isEmpty(self):
        return self.head == -1
    def enqueue(self, data):
        if self.head == self.tail:
            print("full")
        else:
            self.arr[self.tail] = data
            self.tail = (self.tail + 1) % self.size
            if self.head == -1:
                self.head = 0

    def dequeue(self):
        if self.isEmpty():
            print("empty")
        else:
            self.head = (self.head + 1) % self.size
            if self.head == self.tail:
                self.tail = 0
                self.head = -1

    def peek(self):
        if self.isEmpty():
            print("empty")
        else:
            return self.arr[self.head]
    
    def print(self):
        if self.isEmpty():
            print("empty")
        else:
            if self.head < self.tail:
                print(" ".join(map(str,self.arr[self.head:self.tail])))
            else:
                print(" ".join(map(str,self.arr[self.head:] + self.arr[:self.tail])))

q = Queue(5)
for i in range(5):
    q.enqueue(i)
print(q.peek())
q.print()
q.dequeue()
q.dequeue()
q.print()
q.enqueue(6)
q.print()
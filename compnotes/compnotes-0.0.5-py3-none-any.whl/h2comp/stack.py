class Stack():
    def __init__(self, size):
        self.size = size
        self.top = -1
        self.arr = [None] * size

    def isEmpty(self):
        return self.top == -1
    
    def push(self, data):
        if self.top == self.size-1:
            print("full")
        else:
            self.top +=1
            self.arr[self.top] = data
    
    def pop(self):
        if self.top == -1:
            print("empty")
        else:
            self.top -= 1
            return self.arr[self.top+1]
    
    def peek(self):
        return self.arr[self.top] if self.top != -1 else "empty"

s = Stack(2)
s.push(5)
s.push(4)
s.push(3)
print(s.peek())
s.pop()
print(s.peek())
s.pop()
s.pop()
print(s.peek())

    
class HT():
    def __init__(self, size):
        self.arr = [None] * size
        self.size = size

    def findTarget(self, toFind):
        target = hash(toFind) % self.size
        start = target
        while self.arr[target] != toFind:
            target = (target + 1) % self.size
            if target == start:
                return -1
        return target

    def insert(self, data):
        target = self.findTarget(None)
        if target == -1:
            print("full")
        else:
            self.arr[target] = data

    def exists(self, data):
        target = self.findTarget(data)
        return target != -1

    def delete(self, data):
        target = self.findTarget(data)
        if target == -1:
            return False
        else:
            self.arr[target] = None
            return True
    
    def print(self):
        for i in self.arr:
            if i != None:
                print(i)

h = HT(5)
for i in range(6):
    h.insert(i)
print(h.exists(3), h.exists(7))
h.print()
print(h.delete(3))
h.print()


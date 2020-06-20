class Node():
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class CLDLL():
    def __init__(self):
        self.root = None

    def getNode(self, data):
        return Node(data)

    def isEmpty(self):
        return self.root == None

    def insertFront(self, data):
        newNode = self.getNode(data)
        if self.isEmpty():
            self.root = newNode
            newNode.next = newNode
            newNode.prev = newNode
        else:
            newNode.next = self.root
            newNode.prev = self.root.prev
            self.root.prev.next = newNode
            self.root.prev = newNode
            self.root = newNode

    def insertBack(self, data):
        newNode = self.getNode(data)
        if self.isEmpty():
            self.root = newNode
            newNode.next = newNode
            newNode.prev = newNode
        else:
            newNode.next = self.root
            newNode.prev = self.root.prev
            self.root.prev.next = newNode
            self.root.prev = newNode

    def findNode(self, data):
        if self.isEmpty():
            return None
        else:
            curr = self.root
            while True:
                if curr.data != data:
                    curr = curr.next
                else:
                    return curr
                if curr is self.root:
                    return None

    def exists(self, data):
        return self.findNode(data) != None

    def delete(self, data):
        target = self.findNode(data)
        if target:
            if target is self.root and self.root.next is self.root:
                self.root = None
            else:
                target.prev = target.next
                target.next = target.prev
            return True
        else:
            return False
            
    def print(self):
        if self.isEmpty():
            print("empty")
        else:
            curr = self.root
            while True:
                print(curr.data)
                curr = curr.next
                if curr is self.root:
                    break

c = CLDLL()
for i in range(3):
    c.insertFront(i)
print(c.exists(0))
print(c.exists(3))
c.print()
print("break")
print(c.delete(4))
print(c.delete(2))
c.print()
for i in range(4,6):
    c.insertBack(i)
c.print()
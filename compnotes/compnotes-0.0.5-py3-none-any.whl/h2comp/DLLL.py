class DLNode():
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
    def print(self):
        print(self.data)
    
class DLLL():
    def __init__(self):
        self.root = None
    
    def getNode(self, data):
        return DLNode(data)

    def isEmpty(self):
        return self.root == None
    def insertFront(self, data):
        newNode = self.getNode(data)
        if self.isEmpty():
            self.root = newNode
        else:
            newNode.next = self.root
            self.root.prev = newNode
            self.root = newNode

    def insertBack(self, data):
        if self.isEmpty():
            self.insertFront(data)
        else:
            newNode = self.getNode(data)
            curr = self.root
            while curr.next != None:
                curr = curr.next
            curr.next = newNode
            newNode.prev = curr

    def findNode(self, data):
        curr = self.root
        while curr and curr.data != data:
            curr = curr.next
        return curr

    def exists(self, data):
        return self.findNode(data) != None

    def delete(self, data):
        if self.isEmpty():
            return False
        elif self.root.data == data:
            self.root = self.root.next
            return True
        else:
            target = self.findNode(data)
            if target.next:
                target.next.prev = target.prev
                target.prev.next = target.next
                return True
            return False
    
    def print(self):
        curr = self.root
        while curr:
            curr.print()
            curr = curr.next

#some testing
d = DLLL()
d.insertBack(5)
d.insertFront(4)
d.print()
print(d.exists(3), d.exists(4))
d.insertFront(3)
d.insertBack(6)
d.delete(5)
d.print()
            
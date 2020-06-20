class Node():
    def __init__(self, data):
        self.data = data
        self.next = None

    def print(self):
        print(self.data)


class SLLL():
    def __init__(self):
        self.root = None

    def isEmpty(self):
        return self.root == None

    def getNode(self, data):
        return Node(data)

    def insertFront(self, data):
        newNode = self.getNode(data)
        newNode.next = self.root
        self.root = newNode

    def insertBack(self, data):
        if self.isEmpty():
            self.root = self.getNode(data)
        else:
            curr = self.root
            while curr.next != None:
                curr = curr.next
            curr.next = self.getNode(data)

    def exists(self, data):
        curr = self.root
        while curr and curr.data != data:
            curr = curr.next
        return curr != None

    def delete(self, data):
        if self.isEmpty():
            return False
        elif self.root.data == data:
            self.root = self.root.next
            return True
        else:
            curr = self.root
            while curr.next and curr.next.data != data:
                curr = curr.next
            if curr.next == None:
                return False
            else:
                curr.next = curr.next.next
                return True

    def print(self):
        curr = self.root
        while curr != None:
            curr.print()
            curr = curr.next


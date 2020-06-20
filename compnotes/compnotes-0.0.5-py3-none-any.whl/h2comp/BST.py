class Node():
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.tombstone = False

    def minInSubTree(self):
        toCompare = []
        if self.left:
            toCompare.append(self.left.minInSubTree())
        if self.right:
            toCompare.append(self.right.minInSubTree())
        if not self.tombstone:
            toCompare.append(self.data)
        toCompare = list(filter(None, toCompare))
        return min(toCompare) if len(toCompare) != 0 else None

    def maxInSubTree(self):
        toCompare = []
        if self.left:
            toCompare.append(self.left.maxInSubTree())
        if self.right:
            toCompare.append(self.right.maxInSubTree())
        if not self.tombstone:
            toCompare.append(self.data)
        toCompare = list(filter(None, toCompare))
        return max(toCompare) if len(toCompare) != 0 else None

    def preOrder(self):
        print(self.data)
        if self.left:
            self.left.preOrder()
        if self.right:
            self.right.preOrder()

    def inOrder(self):
        if self.left:
            self.left.inOrder()
        print(self.data)
        if self.right:
            self.right.inOrder()

    def postOrder(self):
        if self.left:
            self.left.postOrder()
        if self.right:
            self.right.postOrder()
        print(self.data)

    def print(self):
        datastr = str(self.data)+ ('(T)' if self.tombstone else '')
        left = self.left.data if self.left else "None"
        right = self.right.data if self.right else "None"
        print(f"{datastr:<12}{left:<12}{right:<12}")

class BST():
    def __init__(self):
        self.root = None

    def getNode(self, data):
        return Node(data)
    
    def isEmpty(self):
        return self.root == None

    def insert(self, data):
        if self.isEmpty():
            self.root = self.getNode(data)
        else:
            curr = self.root
            while True:
                if curr.tombstone \
                    and (not curr.left or curr.left.maxInSubTree() == None or curr.left.maxInSubTree() < data) \
                    and (not curr.right or curr.right.minInSubTree() == None or curr.right.minInSubTree() > data):
                    curr.tombstone = False
                    curr.data = data
                    break
                elif data < curr.data:
                    if curr.left:
                        curr = curr.left
                    else:
                        curr.left = self.getNode(data)
                        break
                else:
                    if curr.right:
                        curr = curr.right
                    else:
                        curr.right = self.getNode(data)
                        break
    
    def findNode(self, data):
        curr = self.root
        while curr and curr.data != data:
            if data < curr.data:
                curr = curr.left
            else:
                curr = curr.right
        return curr

    def exists(self, data):
        return self.findNode(data) != None

    def delete(self, data):
        target = self.findNode(data)
        if target:
            target.tombstone = True
            return True
        return False

    def preOrder(self):
        if self.root:
            self.root.preOrder()

    def inOrder(self):
        if self.root:
            self.root.inOrder()

    def postOrder(self):
        if self.root:
            self.root.postOrder()

    def print(self):
        if self.isEmpty():
            print("Empty")
        else:
            queue = [self.root]
            while len(queue) != 0:
                curr = queue.pop()
                if curr != None:
                    queue.append(curr.left)
                    queue.append(curr.right)
                    curr.print()

x = BST()
"""
x.insert(5)
x.insert(3)
x.insert(7)
x.insert(4)
x.insert(2)
x.insert(6)
x.insert(8)
x.delete(7)
"""
x.insert(4)
x.insert(2)
x.insert(6)
x.insert(1)
x.insert(3)
x.insert(5)
x.insert(7)

x.postOrder()

print(x.delete(1))
x.print()
print(x.root.minInSubTree())
print(x.root.right.minInSubTree())

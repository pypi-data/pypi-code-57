import ast
from ast import NodeVisitor, NodeTransformer

verbose = False

class GNode:
    def __init__(self, node):
        self.node = node
        self.visited = False

    def set(self, v):
        self.visited = v

    def __str__(self):
        return self.node.__class__.__name__

    def __eq__(self, other):
        return self.node == other.node

    def __ne__(self, other):
        return self.node != other.node

    def __hash__(self):
        return self.node.__hash__()


def getAllConnectedNodes(nodeGraph, initialNodes):
    nodesToVisit = []
    connectedNodes = set()
    for n in initialNodes:
        nodesToVisit.append(n)
        connectedNodes.add(n)

    while (len(nodesToVisit) > 0):
        gn = nodesToVisit[0]
        nodesToVisit.remove(gn)
        gn.visited = True
        for next in nodeGraph.get(gn, []):
            connectedNodes.add(next)
            if (not next.visited):
                nodesToVisit.append(next)
    return connectedNodes


class DFTransformer(NodeTransformer):
    hotParent = False
    hotNodes = None

    def generic_visit(self, node):
        if (node.__class__.__name__ == "Module"):
            return super().generic_visit(node)
        if (node in self.hotNodes):
            self.hotParent = True
            ret = super().generic_visit(node)
            self.hotParent = False
            return ret
        elif (self.hotParent == True):
            return super().generic_visit(node)
        else:
            return None

    def visitWithContext(self, tree, hotNodes):
        self.hotNodes = hotNodes
        return self.visit(tree)


class PrintTypesTransformer(NodeTransformer):

    def visit_Assign(self, node):
        for child in ast.iter_child_nodes(node):
            self.visit(child)
        retNodes = [node]
        for t in node.targets:
            if hasattr(t, "id"):
                newNode = ast.Expr(value=ast.Call(func=ast.Name(id="print"), args=[
                    ast.BinOp(left=ast.Str(s=t.id + " : "), op=ast.Add(), right=ast.Call(func=ast.Name(id='str'), args=[
                        ast.Call(func=ast.Name(id='type'), args=[ast.Name(id=t.id)], keywords=[])], keywords=[]))],
                                                  keywords=[]))
                retNodes.append(newNode)
        return retNodes

    def visit_Return(self, node):
        for child in ast.iter_child_nodes(node):
            self.visit(child)
        retNodes = []
        if isinstance(node.value, ast.Call) or isinstance(node.value, ast.Expr):
            retNodes = []
            if (verbose == True):
                print("Modify Return Expression")
            tmpId = 'tmp_ret_val'
            newAssign = ast.Assign(targets=[ast.Name(id=tmpId, ctx=ast.Store(), lineno=0, col_offset=0)], value=node.value)
            retNodes.append(newAssign)
            newNode = ast.Expr(value=ast.Call(func=ast.Name(id="print"), args=[
                ast.BinOp(left=ast.Str(s=tmpId + " : "), op=ast.Add(), right=ast.Call(func=ast.Name(id='str'), args=[
                    ast.Call(func=ast.Name(id='type'), args=[ast.Name(id=tmpId)], keywords=[])], keywords=[]))],
                                              keywords=[]))
            retNodes.append(newNode)
            newReturn = ast.Return(value=ast.Name(id=tmpId, ctx=ast.Load(), lineno=0, col_offset=0), lineno=0, col_offset=0)
            retNodes.append(newReturn)
            return retNodes
        else:
            return node


def printNodeGraph(graph):
    for n in graph.keys():
        print(str(n) + " : ", end="")
        for d in graph[n]:
            print(str(d), end=", ")
        print("\n")

from typing import List


class UpdateValueError(Exception):
    """
    Exception raised when user attempts to update the value
    of a node which is not a leaf node.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(
        self,
        expression,
        message="It's forbidden to update the value of non-leaf node type Nodes.",
    ):
        self.expression = expression
        self.message = message


class Node(object):
    CONST_EXCLUDED_KEYS = ["parent"]

    def __init__(
        self,
        key: str,
        name: str,
        description: str = "",
        value: float = 0,
        parent=None,
        children=None,
    ):
        self.key = key
        self.name = name
        self.description = description

        self.children = children
        self.parent = parent
        self.value = value

        # compute the base value of the node
        self.__update_value()

        # check that the keys of the children are correct
        self.__update_children_key()

    def __str__(self):
        return """Key: {0},
         Name: {1}, Description: {2},
         Value: {3}, # of Children: {4}""".format(
            self.key, self.name, self.description, self.value, len(self.children)
        )

    def to_dict(self) -> dict:
        response = {
            "key": self.key,
            "name": self.name,
            "description": self.description,
            "value": self.value,
        }
        response["children"] = [child.to_dict() for child in self.children]
        return response

    @property
    def children(self) -> List["Node"]:
        return self.__children

    @children.setter
    def children(self, children: List["Node"]):
        if children is None:
            self.__children: List["Node"] = []
        else:
            self.__children = children

        # ensure all children have the correct parent set
        for child in self.__children:
            child.parent = self

        # compute the value (since the node is no longer a leaf node)
        self.__update_value()

        # ensure the children's index is correct
        self.__update_children_key()

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: float):
        # this prevents updating parent values directly
        if len(self.children) != 0 and value != 0:
            raise UpdateValueError(
                "Node: {0} has children: {1}".format(self.name, self.children),
            )

        # accept float and int else throw a TypeError
        if type(value) == float:
            self.__value = value
        elif type(value) == int:
            self.__value = float(value)
        else:
            raise TypeError(
                "Expected: value <class 'float | int'>, Received: {0}".format(
                    type(value)
                )
            )

        if hasattr(self, "parent") and self.parent:
            # trigger the recomputing all parent values
            self.parent.__update_value()

    def __update_value(self):
        # only compute value of non-leaf type Nodes
        if len(self.children) != 0:
            # this avoids the setter which would raise an exception
            # since the value of a non-leaf node is update directly
            # -> not sure if this is the best way to do it or
            # if we should just allow updating the value of non-leaf nodes
            # don't replace __value with value!
            self.__value = sum(child.value for child in self.children)

        # only update value of parent if object has a parent attribute
        if hasattr(self, "parent") and self.parent:
            self.parent.__update_value()

    def __update_children_key(self):
        # update the children keys according to their order in the array
        for index, child in enumerate(self.children):
            child.key = self.key + str(index)

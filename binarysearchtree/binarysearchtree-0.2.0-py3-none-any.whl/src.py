import typing as ty
from functools import lru_cache
__all__ = ["BST"]
EMPTY_TREE_ERROR_MESSAGE = "Empty tree has no value."

T = ty.TypeVar("T")
U = ty.TypeVar("U")


class BST(ty.Generic[T]):
    """
    This class represents a frozen Binary Search Tree of distinct, hashable and comparable values.
    """
    def __init__(self, value: ty.Optional[T] = None,
                 left: ty.Optional['BST[T]'] = None,
                 right: ty.Optional['BST[T]'] = None):
        """
        Initializes a binary search tree
        :param value: Value of the current node. If None, the tree is considered empty.
        :param left: Value of the left subtree. Its maximum value must be lesser than that of the current node.
        :param right: Value of the left subtree. Its minimum value must be greater than that of the current node.
        """
        self._value = value
        self._left = left
        self._right = right
        self.__post_init__()

    @property
    def value(self) -> T:
        """
        :return: The current's node Value. None if  empty.
        """
        return self._value

    @property
    def left(self) -> 'BST[T]':
        """
        :return: The left subtree. An empty tree if empty.
        """
        if self._left is None:
            return BST()
        return self._left

    @property
    def right(self) -> 'BST[T]':
        """
        :return: The right subtree. An empty tree if empty.
        """
        if self._right is None:
            return BST()
        return self._right

    @property
    def height(self):
        if self.empty:
            return 0
        else:
            return 1 + max(self.left.height, self.right.height)

    def __post_init__(self):
        if self._left is not None and self._left.empty:
            self._left = None
        if self._right is not None and self._right.empty:
            self._right = None

        if self._value is None:
            assert self._left is None and self._right is None, "When value is None, left and right must be None"

        if self._left is not None:
            assert self.left.max < self._value, "Left subtree must contain lesser values than root"

        if self._right is not None:
            assert self.right.min > self._value, "Right subtree must contain greater values than root"

    @classmethod
    def from_values(cls, values: ty.Iterable[T]) -> 'BST[T]':
        """
        Returns a balanced binary search tree from an iterable.
        :param values: Iterable of values.
        :return: A binary search tree of values.
        """
        sorted_distinct_values = sorted(set(values))
        return cls._from_sorted_distinct_values(sorted_distinct_values)

    @classmethod
    def _from_sorted_distinct_values(cls, values: ty.List[T]) -> 'BST[T]':
        if values:
            length = len(values)
            median_index = length // 2
            median_value = values[median_index]
            left_values = values[: median_index]
            right_values = values[median_index + 1:]
            return BST(median_value, BST._from_sorted_distinct_values(left_values),
                       BST._from_sorted_distinct_values(right_values))
        else:
            return BST()

    @property
    @lru_cache(typed=True)
    def empty(self):
        """
        :return: True if empty, False otherwise.
        """
        return self.value is None

    @property
    @lru_cache(typed=True)
    def min(self) -> T:
        """
        :return: Minimum value of the tree.
        :raises: Value Error if empty.
        """
        if self.empty:
            raise ValueError("Empty tree has no min")
        elif self.left.empty:
            return self.value
        else:
            return self.left.min

    @property
    @lru_cache(typed=True)
    def max(self) -> T:
        """
        :return: Maximum value of the tree.
        :raises: Value Error if empty.
        """
        if self.empty:
            raise ValueError("Empty tree has no max")
        elif self.right.empty:
            return self.value
        else:
            return self.right.max

    @lru_cache(typed=True)
    def __contains__(self, item: T) -> bool:
        """
        Searches an object in the tree.
        :param item: object to search.
        :return: True if exists in the tree, False otherwise.
        """
        return item in self.values

    @property
    @lru_cache(typed=True)
    def values(self) -> ty.FrozenSet[T]:
        """
        All the values of the tree.
        :return: A frozen set of the tree's values.
        """
        if self.empty:
            return frozenset()
        return self.left.values.union(frozenset({self.value})).union(self.right.values)

    @lru_cache(typed=True)
    def closest_to(self, item: T, distance: ty.Callable[[T, T], U]) -> ty.Tuple[T, U]:
        """
        Looks for the closest value to a given item and the distance between the item and the closest value.
        :param item: Object whose closest value is looked for.
        :param distance: A callable returning the distance between two objects. Should be a valid distance.
        :return: A tuple whose first element is the closest value and the second the distance.
        """
        if self.empty:
            raise ValueError(EMPTY_TREE_ERROR_MESSAGE)
        if item in self:
            return item, distance(item, item)
        if (item < self.value and self.left.empty) or (item > self.value and self.right.empty):
            return self.value, distance(item, self.value)
        if item < self.value and item <= self.left.value:
            return self.left.closest_to(item, distance)
        if item > self.value and item > self.right.value:
            return self.right.closest_to(item, distance)
        if item < self.value:
            other = self.left
        else:
            other = self.right
        distance_with_current = distance(item, self.value)
        closest_other, distance_with_closest_other = other.closest_to(item, distance)
        if distance_with_current <= distance_with_closest_other:
            return self.value, distance_with_current
        else:
            return closest_other, distance_with_closest_other

    @lru_cache(typed=True)
    def closest_greater_than(self, value: T) -> T:
        if self.empty:
            raise ValueError(EMPTY_TREE_ERROR_MESSAGE)
        current_value_is_the_closest = (value <= self.value and self.left.empty) or \
                                       (value >= self.value and self.right.empty) or \
                                       (self.value >= value > self.left.closest_greater_than(value))

        if current_value_is_the_closest:
            return self.value
        if value < self.value:
            return self.left.closest_greater_than(value)
        else:
            return self.right.closest_greater_than(value)

    @lru_cache(typed=True)
    def closest_lesser_than(self, value: T) -> T:
        if self.empty:
            raise ValueError(EMPTY_TREE_ERROR_MESSAGE)

        current_value_is_the_closest = (value >= self.value and self.right.empty) or \
                                       (value <= self.value and self.left.empty) or \
                                       (self.value <= value < self.right.closest_lesser_than(value))
        if current_value_is_the_closest:
            return self.value
        if value < self.value:
            return self.left.closest_lesser_than(value)
        else:
            return self.right.closest_lesser_than(value)

    def __eq__(self, other: 'BST[T]') -> bool:
        return type(self) == type(other) and self.value == other.value and self._left == other._left and \
               self._right == other._right

    def __hash__(self):
        return hash((self.value, self._left, self._right))

    def __str__(self):
        value_str = f"value={self.value}"
        left_str = f"left={self._left}"
        right_str = f"right={self._right}"
        return f"BST({value_str}, {left_str}, {right_str})"

    def __repr__(self):
        return str(self)

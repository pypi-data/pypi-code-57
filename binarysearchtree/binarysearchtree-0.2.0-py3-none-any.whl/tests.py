import unittest
from unittest import mock

from binarysearchtree import BST
from hypothesis import given, assume
import hypothesis.strategies as st
import typing as ty
class TestEmptyTree(unittest.TestCase):
    def setUp(self) -> None:
        self.empty_tree = BST()

    def test_empty(self):
        self.assertTrue(self.empty_tree.empty)

    def test_value(self):
        self.assertIsNone(self.empty_tree.value)

    def test_left(self):
        self.assertEqual(self.empty_tree.left, BST())

    def test_right(self):
        self.assertEqual(self.empty_tree.right, BST())

    def test_min(self):
        self.assertRaises(ValueError, lambda: self.empty_tree.min)

    def test_max(self):
        self.assertRaises(ValueError, lambda: self.empty_tree.max)

    def test_values(self):
        self.assertEqual(self.empty_tree.values, frozenset())

    def test_contains(self):
        self.assertNotIn(1, self.empty_tree)
        self.assertNotIn("foo", self.empty_tree)
        self.assertNotIn(-42, self.empty_tree)
        self.assertNotIn("bar", self.empty_tree)

    def test_closest_to(self):
        self.assertRaises(ValueError, lambda: self.empty_tree.closest_to(1, distance=None))

    def test_height(self):
        self.assertEqual(self.empty_tree.height, 0)


class TestLeafBST(unittest.TestCase):
    def setUp(self) -> None:
        self.leaf_one: BST[int] = BST(1)
        self.leaf_foo: BST[str] = BST("foo")

    def test_empty(self):
        self.assertFalse(self.leaf_one.empty)
        self.assertFalse(self.leaf_foo.empty)

    def test_value(self):
        self.assertEqual(self.leaf_one.value, 1)
        self.assertEqual(self.leaf_foo.value, "foo")

    def test_left(self):
        self.assertEqual(self.leaf_one.left, BST())
        self.assertEqual(self.leaf_foo.left, BST())

    def test_right(self):
        self.assertEqual(self.leaf_one.right, BST())
        self.assertEqual(self.leaf_foo.right, BST())

    def test_min(self):
        self.assertEqual(self.leaf_one.min, 1)
        self.assertEqual(self.leaf_foo.min, "foo")

    def test_max(self):
        self.assertEqual(self.leaf_one.max, 1)
        self.assertEqual(self.leaf_foo.max, "foo")

    def test_contains(self):
        self.assertIn(1, self.leaf_one)
        self.assertIn("foo", self.leaf_foo)
        self.assertNotIn(2, self.leaf_one)
        self.assertNotIn("bar", self.leaf_foo)

    def test_values(self):
        self.assertEqual(self.leaf_one.values, frozenset({1}))
        self.assertEqual(self.leaf_foo.values, frozenset({"foo"}))

    def test_closest_to(self):
        spy_float_distance = mock.MagicMock()
        spy_float_distance.return_value = 2
        self.assertEqual(self.leaf_one.closest_to(3, spy_float_distance), (1, 2))
        spy_float_distance.assert_called_once_with(3, 1)
        spy_str_distance = mock.MagicMock()
        spy_str_distance.return_value = 42
        self.assertEqual(self.leaf_foo.closest_to("bar", spy_str_distance), ("foo", 42))
        spy_str_distance.assert_called_once_with("bar", "foo")

    def test_height(self):
        self.assertEqual(self.leaf_one.height, 1)
        self.assertEqual(self.leaf_foo.height, 1)


class TestBST(unittest.TestCase):
    one_leaf = BST(1.)
    three_leaf = BST(3.)

    def setUp(self) -> None:
        self.tree = BST(2., self.one_leaf, self.three_leaf)

    def test_empty(self):
        self.assertFalse(self.tree.empty)

    def test_value(self):
        self.assertEqual(self.tree.value, 2)

    def test_left(self):
        self.assertEqual(self.tree.left, self.one_leaf)

    def test_right(self):
        self.assertEqual(self.tree.right, self.three_leaf)

    def test_min(self):
        self.assertEqual(self.tree.min, 1)

    def test_max(self):
        self.assertEqual(self.tree.max, 3)

    def test_contains(self):
        self.assertIn(1, self.tree)
        self.assertIn(2, self.tree)
        self.assertIn(3, self.tree)

        self.assertNotIn(4, self.tree)
        self.assertNotIn(5, self.tree)
        self.assertNotIn(6, self.tree)

    def test_values(self):
        self.assertEqual(self.tree.values, frozenset({1, 2, 3}))

    def test_closest_to_zero(self):
        spy_float_distance = mock.MagicMock()
        spy_float_distance.side_effect = self.float_distance
        self.assertEqual(self.tree.closest_to(0, spy_float_distance), (1, 1))
        calls_args = spy_float_distance.call_args_list
        expected_calls_args = [mock.call(0, 1)]
        self.assertEqual(calls_args, expected_calls_args)

    def test_closest_to_one_and_three_quarters(self):
        spy_float_distance = mock.MagicMock()
        spy_float_distance.side_effect = self.float_distance
        closest_to, distance = self.tree.closest_to(1.75, spy_float_distance)
        self.assertEqual(closest_to, 2)
        self.assertEqual(distance, 0.25)
        calls_args = spy_float_distance.call_args_list
        expected_calls_args = [mock.call(1.75, 2), mock.call(1.75, 1)]
        self.assertEqual(calls_args, expected_calls_args)

    def test_closest_to_two_and_three_quarters(self):
        spy_float_distance = mock.MagicMock()
        spy_float_distance.side_effect = self.float_distance
        closest_to, distance = self.tree.closest_to(2.75, spy_float_distance)
        self.assertEqual(closest_to, 3)
        self.assertEqual(distance, 0.25)
        calls_args = spy_float_distance.call_args_list
        expected_calls_args = [mock.call(2.75, 2), mock.call(2.75, 3)]
        self.assertEqual(calls_args, expected_calls_args)

    def test_closest_to_two_and_three_quarters_without_three(self):
        spy_float_distance = mock.MagicMock()
        spy_float_distance.side_effect = self.float_distance
        tree = BST(2., BST(1.))
        closest_to, distance = tree.closest_to(2.75, spy_float_distance)
        self.assertEqual(closest_to, 2)
        self.assertEqual(distance, 0.75)
        calls_args = spy_float_distance.call_args_list
        expected_calls_args = [mock.call(2.75, 2)]
        self.assertEqual(calls_args, expected_calls_args)

    def test_closest_to_zero_with_degenerate_tree(self):
        spy_float_distance = mock.MagicMock()
        spy_float_distance.side_effect = self.float_distance
        tree = BST(3, BST(2, BST(1)))
        closest_to, distance = tree.closest_to(0, spy_float_distance)
        self.assertEqual(closest_to, 1)
        self.assertEqual(distance, 1)
        calls_args = spy_float_distance.call_args_list
        expected_calls_args = [mock.call(0, 1)]
        self.assertEqual(calls_args, expected_calls_args)

    def test_closest_to_four_with_degenerate_tree(self):
        spy_float_distance = mock.MagicMock()
        spy_float_distance.side_effect = self.float_distance
        tree = BST(1, None, BST(2, None, BST(3)))
        closest_to, distance = tree.closest_to(4, spy_float_distance)
        self.assertEqual(closest_to, 3)
        self.assertEqual(distance, 1)
        calls_args = spy_float_distance.call_args_list
        expected_calls_args = [mock.call(4, 3)]
        self.assertEqual(calls_args, expected_calls_args)

    def test_closest_greater_than_three_raises_error_with_empty_tree(self):
        tree = BST()
        self.assertRaises(ValueError, lambda: tree.closest_greater_than(3))

    @given(st.integers(), st.integers())
    def test_closest_greater_with_unary_tree_equals_its_value(self, tree_value: int, item: int):
        unary_tree = BST(tree_value)
        self.assertEqual(tree_value, unary_tree.closest_greater_than(item))

    @given(st.lists(st.integers()), st.integers())
    def test_closest_greater_than_is_greater_if_any_value_is_greater(self, values: ty.List[int], item: int):
        assume(any((value >= item for value in values)))
        tree = BST.from_values(values)
        self.assertGreaterEqual(tree.closest_greater_than(item), item)

    @given(st.lists(st.integers()), st.integers())
    def test_closest_greater_than_is_the_minimal_greater_value(self, values: ty.List[int], item: int):
        greater_values = list(filter(lambda x: x >= item, values))
        assume(greater_values)
        tree = BST.from_values(values)
        self.assertEqual(min(greater_values), tree.closest_greater_than(item),
                         msg=(item in tree))

    @given(st.integers())
    def test_closest_lesser_with_empty_tree_raises_exception(self, item):
        bst = BST()
        self.assertRaises(ValueError, lambda:bst.closest_lesser_than(item))

    @given(st.integers(), st.integers())
    def test_closest_lesser_with_unary_tree_equals_its_value(self, tree_value: int, item: int):
        unary_tree = BST(tree_value)
        self.assertEqual(tree_value, unary_tree.closest_lesser_than(item))

    @given(st.lists(st.integers()), st.integers())
    def test_closest_lesser_than_is_lesser_if_any_value_is_lesser(self, values: ty.List[int], item: int):
        assume(any((value <= item for value in values)))
        tree = BST.from_values(values)
        self.assertLessEqual(tree.closest_lesser_than(item), item)

    @given(st.lists(st.integers()), st.integers())
    def test_closest_lesser_than_is_the_maximal_lesser_value(self, values: ty.List[int], item: int):
        lesser_values = list(filter(lambda x: x <= item, values))
        assume(lesser_values)
        tree = BST.from_values(values)
        self.assertEqual(max(lesser_values), tree.closest_lesser_than(item),
                         msg=tree)

    def test_height(self):
        self.assertEqual(self.tree.height, 2)

    @staticmethod
    def float_distance(a, b):
        return abs(a - b)


class TestIncorrectBST(unittest.TestCase):
    def test_left_greater_than_root(self):
        self.assertRaises(AssertionError, lambda: BST(1, left=BST(2)))
        self.assertRaises(AssertionError, lambda: BST(1, left=BST(0, None, BST(3))))

    def test_right_lesser_than_root(self):
        self.assertRaises(AssertionError, lambda: BST(1, right=BST(0)))
        self.assertRaises(AssertionError, lambda: BST(1, right=BST(2, BST(0))))


class TestFromValues(unittest.TestCase):
    def test_from_empty(self):
        self.assertEqual(BST.from_values([]), BST())

    def test_from_one_value(self):
        self.assertEqual(BST.from_values([1]), BST(1))

    def test_from_two_distinct_value(self):
        expected_bst = BST(2, BST(1))
        self.assertEqual(BST.from_values([1, 2]), expected_bst)
        self.assertEqual(BST.from_values([2, 1]), expected_bst)
        self.assertEqual(BST.from_values([1, 2, 1]), expected_bst)

    def test_from_three_distinct_values(self):
        expected_bst = BST(2, BST(1), BST(3))
        self.assertEqual(BST.from_values([1, 2, 3]), expected_bst)
        self.assertEqual(BST.from_values([3, 2, 1]), expected_bst)
        self.assertEqual(BST.from_values([2, 1, 3]), expected_bst)
        self.assertEqual(BST.from_values([2, 1, 3, 3]), expected_bst)

        expected_bst = BST(10, BST(5), BST(42))
        self.assertEqual(BST.from_values([10, 42, 5]), expected_bst)

    def test_from_four_distinct_values(self):
        expected_bst = BST(3, BST(2, BST(1)), BST(4))
        self.assertEqual(BST.from_values([1, 2, 3, 4]), expected_bst)

    def test_from_five_distinct_values(self):
        expected_bst = BST(3, BST(2, BST(1)), BST(5, BST(4)))
        self.assertEqual(BST.from_values([1, 2, 3, 4, 5]), expected_bst)

    def test_from_six_distinct_values(self):
        expected_bst = BST(4, BST(2, BST(1), BST(3)), BST(6, BST(5)))
        self.assertEqual(BST.from_values([1, 2, 3, 4, 5, 6]), expected_bst)

    def test_from_seven_distinct_values(self):
        expected_bst = BST(4, BST(2, BST(1), BST(3)), BST(6, BST(5), BST(7)))
        self.assertEqual(BST.from_values([1, 2, 3, 4, 5, 6, 7 ]), expected_bst)


class TestUnbalancedTree(unittest.TestCase):
    tree = BST(10, None, BST(15, None, BST(20)))

    def test_height(self):
        self.assertEqual(self.tree.height, 3)


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import MagicMock

from depgraph import ExecutableDirectedMultiGraph


class TestExecutableDirectedMultiGraph(unittest.TestCase):
    def test_fully_executable_true(self):
        nodes = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4)]

        g = ExecutableDirectedMultiGraph()
        for n in nodes:
            g.add_node(n, function=MagicMock())

        g.add_edges_from(edges)

        self.assertTrue(g.is_fully_executable())

    def test_fully_executable_false(self):
        edges = [(1, 2), (2, 3), (3, 4)]

        g = ExecutableDirectedMultiGraph()
        g.add_node(1)
        g.add_node(2, function=MagicMock())
        g.add_node(3, function=MagicMock())
        g.add_node(4, function=MagicMock())
        g.add_edges_from(edges)

        self.assertFalse(g.is_fully_executable())

    def test_node_function_not_callable(self):
        edges = [(1, 2), (2, 3), (3, 4)]

        g = ExecutableDirectedMultiGraph()
        g.add_node(1, function=MagicMock())
        g.add_node(2, function="I am not callable, but a string")
        g.add_node(3, function=MagicMock())
        g.add_node(4, function=MagicMock())
        g.add_edges_from(edges)

        self.assertFalse(g.is_fully_executable())

    def test_graph_has_cycle(self):
        nodes = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (4, 3)]

        g = ExecutableDirectedMultiGraph()
        for n in nodes:
            g.add_node(n, function=MagicMock())

        g.add_edges_from(edges)

        self.assertFalse(g.is_fully_executable())

    def test_execution_order(self):
        nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        edges = [(1, 2), (2, 4), (2, 5), (3, 4), (4, 6), (5, 6), (6, 7), (8, 7), (9, 7), (7, 0)]

        g = ExecutableDirectedMultiGraph()
        for n in nodes:
            g.add_node(n, function=MagicMock())

        g.add_edges_from(edges)

        order = g.get_execution_order(g)
        first = set(order[:4])
        second = order[4]
        third = set(order[5:7])
        last = set(order[7:])

        self.assertSetEqual(first, {1, 3, 8, 9})
        self.assertEqual(second, 2)
        self.assertSetEqual(third, {4, 5})
        self.assertSetEqual(last, {6, 7, 0})

    def test_execution(self):
        g = ExecutableDirectedMultiGraph()

        first_mock = MagicMock()
        second_mock = MagicMock()

        g.add_node(1, function=first_mock, function_arguments=[1, 2])
        g.add_node(2, function=second_mock)

        g.add_edge(1, 2)

        g.execute()

        first_mock.assert_called_once_with(1, 2, context={})
        second_mock.assert_called_once()

    def test_execution_context(self):
        g = ExecutableDirectedMultiGraph()

        first_mock = MagicMock(return_value=4)
        second_mock = MagicMock()

        g.add_node(1, function=first_mock, function_arguments=[1, 2])
        g.add_node(2, function=second_mock)

        g.add_edge(1, 2)

        g.execute()

        first_mock.assert_called_once_with(1, 2, context={})
        second_mock.assert_called_once_with(context={1: 4})
if __name__ == "__main__":
    unittest.main()
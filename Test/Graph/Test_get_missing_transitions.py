import unittest

from lazr.restfulclient.resource import missing

from Graph import Graph
from State import State
from Transition import Transition


class MyTestCase(unittest.TestCase):
    def test_get_missing_transitions(self):
        G_before_merge = Graph()
        G_before_merge.graph = {
            State(1): {State(2): [Transition(1 ,2,'a / 1')],
                       State(4):[Transition(1, 4, 'b / 1')]},
            State(2): {State(3): [Transition(2, 3, 'b / 1')]},
            State(3): {},
            State(4): {State(5):[Transition(4, 5, 'a / 1')],
                       State(6):[Transition(4, 6, 'b / 1')]},
            State(5): {},
            State(6): {}
        }

        G_after_merge = Graph()
        G_after_merge.graph = {
            State(1): {State(4): [Transition(1, 4, 'b / 1'),
                                  Transition(1, 2, 'a / 1')]},
            State(3): {},
            State(4): {State(5): [Transition(4, 5, 'a / 1')],
                       State(6): [Transition(4, 6, 'b / 1')]},
            State(5): {},
            State(6): {}
        }

        missing_transitions = G_after_merge.get_missing_transitions(G_before_merge, State(4), [State(2)])
        expected_result = []
        self.assertEqual(expected_result, missing_transitions)  # add assertion here


if __name__ == '__main__':
    unittest.main()

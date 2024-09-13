import unittest

from Graph import Graph
from State import State
from Transition import Transition
from Utilities.Pattern import dfs_find_states


class MyTestCase(unittest.TestCase):
    def test_no_branches(self):
        G = Graph()
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        state4 = State(4)
        state5 = State(5)
        state6 = State(6)
        state7 = State(7)

        G.graph = {state1: {state2: [Transition(state1, state2, 'a/1')]},
                   state2: {state3: [Transition(state2, state3, 'a/2')]},
                   state3: {state4: [Transition(state3, state4, 'b/1')]},
                   state4: {state5: [Transition(state4, state5, 'b/2')]},
                   state5: {state6: [Transition(state5, state6, 'a/1')]},
                   state6: {state7: [Transition(state6, state7, 'a/2')]},
                   state7: {}}
        state_with_event_p = dfs_find_states(G, state1, 'b/2')
        self.assertEqual(state4, state_with_event_p)  # add assertion here


if __name__ == '__main__':
    unittest.main()

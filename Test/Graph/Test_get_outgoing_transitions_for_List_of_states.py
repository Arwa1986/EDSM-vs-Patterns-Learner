import unittest

from State import State
from Transition import Transition
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):
        positive_traces = [['a/1', 'a/2', 'b/1', 'b/1'], ['a/1', 'a/1', 'b/1'], ['a/1', 'a/2', 'b/1', 'a/1']]
        self.pta = PTA()
        self.pta.build_pta(positive_traces)

    def test_states_with_transitions_of_the_same_label(self):
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state5 = State(5)
        transition0 = Transition(state0, state1, 'a/1')
        transition1 = Transition(state1, state2, 'a/2')
        transition2 = Transition(state1, state5, 'a/1')
        result = self.pta.G.get_outgoing_transitions_for_list_of_states([state0, state1])

        self.assertEqual([transition0, transition1, transition2], result)  # add assertion here


if __name__ == '__main__':
    unittest.main()

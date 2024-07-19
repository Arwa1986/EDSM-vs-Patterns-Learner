import unittest

from State import State
from Transition import Transition
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):
        positive_traces = [['a/1', 'a/2', 'b/1', 'b/1'], ['a/1', 'a/1', 'b/1'], ['a/1', 'a/2', 'b/1', 'a/1']]
        self.pta = PTA()
        self.pta.build_pta(positive_traces)

    def test_state_with_one_incoming_transition(self):
        state0 = State(0)
        state1 = State(1)
        transition0 = Transition(state0, state1, 'a/1')
        result = self.pta.G.has_incoming_transition_label(state0, transition0)

        self.assertEqual(True, result)  # add assertion here

    def test_state_has_incoming_transition_with_label_but_different_traget(self):
        state0 = State(0)
        state1 = State(1)
        transition0 = Transition(state0, state0, 'a/1')
        result = self.pta.G.has_incoming_transition_label(state0, transition0)

        self.assertEqual(True, result)  # add assertion here

if __name__ == '__main__':
    unittest.main()

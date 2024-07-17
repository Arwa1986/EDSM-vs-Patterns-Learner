import unittest

from State import State
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):

        positive_traces = [['a/1', 'a/2', 'b/1', 'b/1'], ['a/1', 'a/1', 'b/1'],['a/1', 'a/2', 'b/1', 'a/1']]
        self.pta = PTA()
        self.pta.build_pta(positive_traces)

    def test_states_with_the_same_outgoing_transition(self):
        state2 = State(2)
        state5 = State(5)
        common_labels = self.pta.G.have_shared_outgoing_transition(state2, state5)

        self.assertEqual(['b/1'], common_labels)  # add assertion here

    def test_states_with_the_different_outgoing_transition(self):
        state1 = State(1)
        state5 = State(5)
        common_labels = self.pta.G.have_shared_outgoing_transition(state1, state5)

        self.assertEqual([], common_labels)  # add assertion here
    def test_states_with_the_shared_outgoing_transition(self):
        state1 = State(1)
        state3= State(3)
        common_labels = self.pta.G.have_shared_outgoing_transition(state1, state3)

        self.assertEqual(['a/1'], common_labels)  # add assertion here

if __name__ == '__main__':
    unittest.main()

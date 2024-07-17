import unittest

from State import State
from Utilities.EDSM import EDSM
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):

        positive_traces = [['a/1', 'a/2', 'b/1', 'b/1'], ['a/1', 'a/1', 'b/1']]
        self.pta = PTA()
        self.pta.build_pta(positive_traces)
    def test_leaf_state(self):
        state4 = State(4)
        result = self.pta.G.get_descendants(state4)
        self.assertEqual([], result)  # add assertion here

    def test_state_with_children_only(self):
        state3 = State(3)
        state4 = State(4)

        result = self.pta.G.get_descendants(state3)
        self.assertEqual([state4], result)  # add assertion here

    def test_state_with_children_of_children(self):
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        state4 = State(4)
        state5 = State(5)
        state6 = State(6)

        result = self.pta.G.get_descendants(state1)
        self.assertEqual([state2, state3, state4, state5, state6], result)  # add assertion here
if __name__ == '__main__':
    unittest.main()

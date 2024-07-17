import unittest

from State import State
from Transition import Transition
from Utilities.EDSM import EDSM
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.state0 = State(0)
        self.state1 = State(1)
        self.state2 = State(2)
        self.state5 = State(5)

        positive_traces = [['a/1', 'a/2', 'b/1', 'b/1'], ['a/1', 'a/1', 'b/1']]
        self.pta = PTA()
        self.pta.build_pta(positive_traces)
    def test_blue_is_a_child_of_the_root(self):
        edsm = EDSM(self.pta)
        edsm.pick_next_blue(self.state0)

        expected_result = [self.state1]

        self.assertEqual(expected_result, edsm.blue_states)  # add assertion here

    def test_blue_is_not_a_child_of_the_root(self):
        edsm = EDSM(self.pta)
        edsm.red_states.append(self.state1)
        edsm.pick_next_blue(self.state0)

        expected_result = [self.state2, self.state5]

        self.assertEqual(expected_result, edsm.blue_states)  # add assertion here

if __name__ == '__main__':
    unittest.main()

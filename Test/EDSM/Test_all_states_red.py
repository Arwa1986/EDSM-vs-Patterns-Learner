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
        self.state3 = State(3)
        self.state4 = State(4)

        transition1 = Transition(self.state0, self.state1, 'a/1')
        transition2 = Transition(self.state1, self.state2, 'a/2')
        transition3 = Transition(self.state2, self.state3, 'b/1')
        transition4 = Transition(self.state3, self.state4, 'b/1')
        actual_graph = {
            self.state0: {self.state1: [transition1]},
            self.state1: {self.state2: [transition2]},
            self.state2: {self.state3: [transition3]},
            self.state3: {self.state4: [transition4]},
            self.state4: {}
        }

        positive_traces = [['a/1', 'a/2', 'b/1', 'b/1']]
        self.pta = PTA()
        self.pta.build_pta(positive_traces)
    def test_just_the_root_is_red(self):
        edsm = EDSM(self.pta)
        result = edsm.is_all_states_red()

        self.assertEqual(result, False)  # add assertion here

    def test_all_states_are_red(self):
        edsm = EDSM(self.pta)
        edsm.red_states.append(self.state1)
        edsm.red_states.append(self.state2)
        edsm.red_states.append(self.state3)
        edsm.red_states.append(self.state4)
        result = edsm.is_all_states_red()

        self.assertEqual(result, True)  # add assertion here

    def test_some_states_are_red(self):
        edsm = EDSM(self.pta)
        edsm.red_states.append(self.state1)
        edsm.red_states.append(self.state3)
        result = edsm.is_all_states_red()

        self.assertEqual(result, False)  # add assertion here
if __name__ == '__main__':
    unittest.main()

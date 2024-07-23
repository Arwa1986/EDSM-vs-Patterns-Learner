import unittest

from Graph import Graph
from State import State
from Transition import Transition
from Utilities.EDSM import EDSM
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):
        G = Graph()

        self.state0 = State(0)
        self.state1 = State(1)
        self.state2 = State(2)
        self.state3 = State(3)
        self.state4 = State(4)
        self.state5 = State(5)
        self.state6 = State(6)

        self.state4.color = 'red'
        self.state0.color = 'red'
        self.state1.color = 'red'
        transition1 = Transition(self.state0, self.state1, 'a/1')
        transition2 = Transition(self.state1, self.state2, 'a/2')
        transition3 = Transition(self.state2, self.state3, 'b/1')
        transition4 = Transition(self.state1, self.state2, 'b/1')
        transition5 = Transition(self.state1, self.state1, 'a/1')
        transition6 = Transition(self.state5, self.state6, 'b/1')
        G.graph = {
            self.state0: {self.state1: [transition1]},
            self.state1: {self.state2: [transition2, transition4], self.state1: [transition5]},
            self.state2: {self.state3: [transition3]},
            self.state3: {self.state4: [transition4]},
            self.state4: {},
            self.state5: {self.state6: [transition6]},
            self.state6: {}
        }

        G.initial_state

        pta = PTA()
        pta.G = G
        self.edsm = EDSM(pta)

    def test_some_states_are_red(self):
        # self.edsm.pta.G.get_state_for_label(0).color = 'red'
        # self.edsm.pta.G.get_state_for_label(1).color = 'red'
        # self.edsm.pta.G.get_state_for_label(4).color = 'red'
        self.edsm.update_red_states()
        actual_result = self.edsm.red_states
        expected_result = [self.state0, self.state1, self.state4]
        self.assertEqual(actual_result, expected_result)

    def test_some_states_are_red(self):
        self.edsm.pta.G.get_state_for_label(2).color = 'red'
        self.edsm.update_red_states()
        actual_result = self.edsm.red_states
        expected_result = [self.state0, self.state1, self.state2, self.state4]
        self.assertEqual(actual_result, expected_result)
if __name__ == '__main__':
    unittest.main()
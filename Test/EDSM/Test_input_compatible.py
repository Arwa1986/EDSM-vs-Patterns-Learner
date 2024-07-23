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
        transition3 = Transition(self.state2, self.state3, 'b/2')
        transition4 = Transition(self.state1, self.state2, 'b/1')
        transition5 = Transition(self.state1, self.state1, 'a/1')
        transition6 = Transition(self.state5, self.state6, 'b/1')
        G.graph = {
            self.state0: {self.state1: [transition1]},
            self.state1: {self.state2: [transition2, transition4]},
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

    def test_states_with_same_input_different_output(self):
        compatible = self.edsm.is_input_compatible([self.state2, self.state5])
        self.assertFalse(compatible, 'states are not input compatible')  # add assertion here

    def test_states_with_same_input_same_output(self):
        compatible = self.edsm.is_input_compatible([self.state3, self.state5])
        self.assertTrue(compatible, 'states are not input compatible')  # add assertion here

    def test_states_with_different_input_same_output(self):
        compatible = self.edsm.is_input_compatible([self.state0, self.state5])
        self.assertTrue(compatible, 'states are not input compatible')

    def test_states_with_different_input_different_output(self):
        compatible = self.edsm.is_input_compatible([self.state0, self.state2])
        self.assertTrue(compatible, 'states are not input compatible')

if __name__ == '__main__':
    unittest.main()

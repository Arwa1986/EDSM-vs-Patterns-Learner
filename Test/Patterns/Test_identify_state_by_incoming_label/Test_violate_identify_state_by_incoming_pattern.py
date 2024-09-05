import unittest

from Graph import Graph
from State import State
from Transition import Transition
from Utilities.EDSM import EDSM
from Utilities.PTA import PTA
from Utilities.Pattern import violate_identify_state_by_incoming_label_pattern


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

        self.transition1 = Transition(self.state0, self.state1, 'a/1')
        self.transition2 = Transition(self.state0, self.state2, 'b/2')
        self.transition3 = Transition(self.state2, self.state3, 'b/1')
        self.transition4 = Transition(self.state2, self.state1, 'a/1')
        self.transition5 = Transition(self.state3, self.state4, 'a/2')
        self.transition6 = Transition(self.state3, self.state5, 'b/2')
        self.transition7 = Transition(self.state4, self.state4, 'b/1')
        self.transition8 = Transition(self.state4, self.state1, 'a/1')
        G.graph = {
            self.state0: {self.state1: [self.transition1],
                          self.state2: [self.transition2]},
            self.state1: {},

            self.state2: {self.state3: [self.transition3],
                          self.state1: [self.transition4]},

            self.state3: {self.state4: [self.transition5],
                          self.state5: [self.transition6]},

            self.state4: {self.state4: [self.transition7],
                          self.state1: [self.transition8]},

            self.state5: {}
        }

        G.set_initial_state(self.state0)
        pta = PTA()
        pta.G = G
        self.edsm = EDSM(pta)

        self.identifiable_states = [(self.state1, 'a/1'), (self.state4, 'a/2')]

    def test_automata_with_no_violation(self):
        self.state0.color = 'red'
        self.state1.color = 'red'
        self.state2.color = 'red'
        self.state3.color = 'red'
        self.state4.color = 'red'
        self.state5.color = 'red'
        self.edsm.update_red_states()
        states_violate_pattern = violate_identify_state_by_incoming_label_pattern(self.edsm, self.identifiable_states)
        self.assertEqual([], states_violate_pattern)  # add assertion here

    def test_automata_with_violation(self):
        G = Graph()

        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        state4 = State(4)
        state5 = State(5)
        state0.color = 'red'
        state1.color = 'red'
        state2.color = 'red'
        state3.color = 'red'
        state4.color = 'blue'
        state5.color = 'blue'

        transition1 = Transition(state0, state1, 'a/1')
        transition2 = Transition(state0, state2, 'b/2')
        transition3 = Transition(state2, state3, 'a/1')
        transition4 = Transition(state2, state5, 'b/1')
        transition5 = Transition(state3, state4, 'b/1')
        transition6 = Transition(state3, state1, 'a/1')
        transition7 = Transition(state4, state4, 'b/1')
        transition8 = Transition(state4, state1, 'a/1')
        G.graph = {
            state0: {state1: [transition1],
                     state2: [transition2]},
            state1: {},

            state2: {state3: [transition3],
                     state5: [transition4]},

            state3: {state4: [transition5],
                     state1: [transition6]},

            state4: {state4: [transition7],
                     state1: [transition8]},

            state5: {}
        }

        G.set_initial_state(state0)
        pta = PTA()
        pta.G = G
        edsm = EDSM(pta)

        identifiable_states = [(state1, 'a/1'), (state4, 'a/2')]

        edsm.update_red_states()
        states_violate_pattern = violate_identify_state_by_incoming_label_pattern(edsm, identifiable_states)
        self.assertEqual([([state1, state3], 'a/1')], states_violate_pattern)  # add assertion here
if __name__ == '__main__':
    unittest.main()

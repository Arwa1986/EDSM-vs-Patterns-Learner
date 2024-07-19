import unittest

from State import State
from Transition import Transition
from Utilities.EDSM import EDSM
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):
        positive_traces = [['a/1', 'a/2', 'b/1', 'b/1'], ['a/1', 'a/1', 'b/1']]
        self.pta = PTA()
        self.pta.build_pta(positive_traces)

    def test_something(self):
        edsm = EDSM(self.pta)
        source_state = self.pta.G.get_state_for_label(5)
        target_state = self.pta.G.get_state_for_label(1)

        edsm.transfer_out_edge(source_state, target_state)

        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        state4 = State(4)
        state5 = State(5)
        state6 = State(6)

        transition1 = Transition(state0, state1, 'a/1')
        transition2 = Transition(state1, state2, 'a/2')
        transition3 = Transition(state2, state3, 'b/1')
        transition4 = Transition(state3, state4, 'b/1')
        transition5 = Transition(state1, state5, 'a/1')
        transition6 = Transition(state1, state6, 'b/1')
        expeted_graph = {
            state0: {state1: [transition1]},
            state1: {state2: [transition2], state5:[transition5], state6: [transition6]},
            state2: {state3: [transition3]},
            state3: {state4: [transition4]},
            state4: {},
            state5: {},
            state6: {}
        }
        new_pta = PTA()
        new_pta.G.graph = expeted_graph
        new_pta.G.initial_state = state0

        self.assertEqual(new_pta.G, self.pta.G)  # add assertion here


if __name__ == '__main__':
    unittest.main()

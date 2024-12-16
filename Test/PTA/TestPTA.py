import unittest

from State import State
from Transition import Transition
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def test_add_a_trace_to_empty_graph(self):
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        state4 = State(4)

        transition1 = Transition(state0, state1, 'a / 1')
        transition2 = Transition(state1, state2, 'a / 2')
        transition3 = Transition(state2, state3, 'b / 1')
        transition4 = Transition(state3, state4, 'b / 1')
        expected_graph = {
            state0 : {state1:[transition1]},
            state1 :{state2:[transition2]},
            state2 : {state3:[transition3]},
            state3 : {state4:[transition4]},
            state4 : {state4:[Transition(state4, state4, 'to_be_continued / add_transition')]}
        }

        positive_traces= [['a / 1', 'a / 2', 'b / 1', 'b / 1']]
        pta = PTA()
        pta.build_pta(positive_traces)

        self.assertEqual(expected_graph, pta.G.graph)  # add assertion here

    def test_add_a_trace_to_non_empty_graph(self):
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        state4 = State(4)
        state5 = State(5)
        state6 = State(6)

        transition1 = Transition(state0, state1, 'a / 1')
        transition2 = Transition(state1, state2, 'a / 2')
        transition3 = Transition(state2, state3, 'b / 1')
        transition4 = Transition(state3, state4, 'b / 1')
        transition5 = Transition(state1, state5, 'a / 1')
        transition6 = Transition(state5, state6, 'b / 1')

        expected_graph = {
            state0 : {state1:[transition1]},
            state1 : {state2:[transition2], state5:[transition5]},
            state2 : {state3:[transition3]},
            state3 : {state4:[transition4]},
            state4 : {state4:[Transition(state4, state4, 'to_be_continued / add_transition')]},
            state5 : {state6 : [transition6]},
            state6 : {state6:[Transition(state6, state6, 'to_be_continued / add_transition')]}
        }

        test_graph = {
            state0: {state1: [transition1]},
            state1: {state2: [transition2]},
            state2: {state3: [transition3]},
            state3: {state4: [transition4]},
            state4: {state4:[Transition(state4, state4, 'to_be_continued / add_transition')]}
        }
        pta = PTA()
        pta.G.graph = test_graph
        pta.G.set_initial_state(state0)
        pta.current_state_id = 4
        pta.add_trace(['a / 1', 'a / 1', 'b / 1'])
        self.assertEqual(expected_graph, pta.G.graph)  # add assertion here
if __name__ == '__main__':
    unittest.main()

import re
import unittest

from Form_Converters.Dictionary_NuSMV_converter import dictionary_to_NuSMV
from Graph import Graph
from State import State
from Transition import Transition


class MyTestCase(unittest.TestCase):
    def test_convert_dictionary_to_NuSMV(self):
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
        transition5 = Transition(state1, state5, 'b/1')
        transition6 = Transition(state5, state6, 'a/1')
        transition7 = Transition(state0, state0, 'b/1')

        graph_dictionary = {
            state0: {state1: [transition1], state0:[transition7]},
            state1: {state2: [transition2], state5: [transition5]},
            state2: {state3: [transition3]},
            state3: {state4: [transition4]},
            state4: {},
            state5: {state6: [transition6]},
            state6: {}
        }

        self.G = Graph()
        self.G.set_initial_state(state0)
        self.G.set_input_alphabet(['a','b'])
        self.G.set_output_alphabet([1,2])
        self.G.graph = graph_dictionary

        graph_NuSMV_str = dictionary_to_NuSMV(self.G)

        expected_output_str = ('MODULE main'
                               'VAR'
                               'state:{State(0), State(1), State(2), State(3), State(4), State(5), State(6)};'
                               'input:{a, b};'
                               'output:{1, 2};'
                               'ASSIGN'
                               'init(state):=State(0);'
                               'next(state):=case'
                                'state = State(0) & input = a : State(1);'
                                'state = State(0) & input = b : State(0);'
                                'state = State(1) & input = a : State(2);'
                                'state = State(1) & input = b : State(5);'
                                'state = State(2) & input = b : State(3);'
                                'state = State(3) & input = b : State(4);'
                                'state = State(5) & input = a : State(6);'
                                'esac;'
                                'next(output):=case'
                                'state = State(0) & input = a : 1;'
                                'state = State(0) & input = b : 1;'
                                'state = State(1) & input = a : 2;'
                                'state = State(1) & input = b : 1;'
                                'state = State(2) & input = b : 1;'
                                'state = State(3) & input = b : 1;'
                                'state = State(5) & input = a : 1;'
                                'esac;')

        # compare the result with the expected output
        # Remove all white spaces, tabs, and new lines
        actual_str_clean = re.sub(r'\s+', '', graph_NuSMV_str)
        expected_str_clean = re.sub(r'\s+', '', expected_output_str)

        # print(graph_NuSMV_str)
        self.assertEqual(True, actual_str_clean==expected_str_clean)  # add assertion here

if __name__ == '__main__':
    unittest.main()

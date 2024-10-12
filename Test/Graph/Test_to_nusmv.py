import re
import unittest

from Graph import Graph
from State import State
from Transition import Transition


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.state0 = State(0)
        self.state1 = State(1)
        self.state2 = State(2)
        state3 = State(3)
        state4 = State(4)
        state5 = State(5)
        state6 = State(6)

        transition1 = Transition(self.state0, self.state1, 'a / 1')
        transition2 = Transition(self.state1, self.state2, 'a / 2')
        transition3 = Transition(self.state2, state3, 'b / 1')
        transition4 = Transition(state3, state4, 'b / 1')
        transition5 = Transition(self.state1, state5, 'b / 1')
        transition6 = Transition(state5, state6, 'a / 1')
        transition7 = Transition(self.state0, self.state0, 'b / 1')

        graph_dictionary = {
            self.state0: {self.state1: [transition1], self.state0: [transition7]},
            self.state1: {self.state2: [transition2], state5: [transition5]},
            self.state2: {state3: [transition3]},
            state3: {state4: [transition4]},
            state4: {},
            state5: {state6: [transition6]},
            state6: {}
        }

        self.G = Graph()
        self.G.set_initial_state(self.state0)
        self.G.set_input_alphabet(['a', 'b'])
        self.G.set_output_alphabet([1, 2])
        self.G.graph = graph_dictionary
    def test_convert_model(self):
        graph_NuSMV_str = self.G.to_nusmv(self.G.get_all_states(), ['F (input = a ->X state = 1'])
        expected_output_str = ('MODULE main'
                               'VAR'
                               'state:{0, 1, 2, 3,4,5,6};'
                               'input:{a, b};'
                               'output:{1, 2};'
                               'ASSIGN'
                               'init(state):=0;'
                               'next(state):=case'
                               'state = 0 & input = a : 1;'
                               'state = 0 & input = b : 0;'
                               'state = 1 & input = a : 2;'
                               'state = 1 & input = b : 5;'
                               'state = 2 & input = b : 3;'
                               'state = 3 & input = b : 4;'
                               'state = 5 & input = a : 6;'
                               'TRUE : state;'
                               'esac;'
                               'output:=case'
                               'state = 0 & input = a : 1;'
                               'state = 0 & input = b : 1;'
                               'state = 1 & input = a : 2;'
                               'state = 1 & input = b : 1;'
                               'state = 2 & input = b : 1;'
                               'state = 3 & input = b : 1;'
                               'state = 5 & input = a : 1;'
                               'TRUE : state;'
                               'esac;'
                               'LTLSPEC F (input = a ->X state = 1;')

        # compare the result with the expected output
        # Remove all white spaces, tabs, and new lines
        actual_str_clean = re.sub(r'\s+', '', graph_NuSMV_str)
        expected_str_clean = re.sub(r'\s+', '', expected_output_str)

        # print(graph_NuSMV_str)
        self.assertEqual(True, actual_str_clean == expected_str_clean)  # add assertion here

    def test_convert_partial_model(self):
        graph_NuSMV_str = self.G.to_nusmv([self.state0, self.state1, self.state2], ['F (input = a ->X state = 1)'])
        expected_output_str = ('MODULE main'
                               'VAR'
                               'state:{0, 1, 2};'
                               'input:{a, b};'
                               'output:{1, 2};'
                               'ASSIGN'
                               'init(state):=0;'
                               'next(state):=case'
                               'state = 0 & input = a : 1;'
                               'state = 0 & input = b : 0;'
                               'state = 1 & input = a : 2;'
                               'TRUE : state;'
                               'esac;'
                               'output:=case'
                               'state = 0 & input = a : 1;'
                               'state = 0 & input = b : 1;'
                               'state = 1 & input = a : 2;'
                               'TRUE : state;'
                               'esac;'
                               'LTLSPEC F (input = a ->X state = 1);')

        # compare the result with the expected output
        # Remove all white spaces, tabs, and new lines
        actual_str_clean = re.sub(r'\s+', '', graph_NuSMV_str)
        expected_str_clean = re.sub(r'\s+', '', expected_output_str)

        # print(graph_NuSMV_str)
        self.assertEqual(True, actual_str_clean == expected_str_clean)  # add assertion here

if __name__ == '__main__':
    unittest.main()

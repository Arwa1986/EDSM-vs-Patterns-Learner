import unittest

from State import State
from Transition import Transition
from Utilities.Dictionary_Networkx_Converter import dictionary_to_networkx


class MyTestCase(unittest.TestCase):
    def test_convert_dictionary_to_networkx(self):
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
        transition6 = Transition(state5, state6, 'b/1')

        graph_dictionary = {
            state0: {state1: [transition1]},
            state1: {state2: [transition2], state5: [transition5]},
            state2: {state3: [transition3]},
            state3: {state4: [transition4]},
            state4: {},
            state5: {state6: [transition6]},
            state6: {}
        }

        graph_networks = dictionary_to_networkx(graph_dictionary)

        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

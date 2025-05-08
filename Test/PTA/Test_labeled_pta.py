import unittest

from Graph import Graph
from State import State
from Transition import Transition
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.RefDFA_G = Graph()
        self.RefDFA_G.graph={
            State(0): {State(1):[Transition(0, 1, 'open / 1')],
                       State(0):[Transition(0, 0, 'load / 1')]
                       },
            State(1): {State(2):[Transition(1, 2, 'edit / 1')],
                       State(0):[Transition(1, 0, 'exit / 2')]
                    },
            State(2): {State(1):[Transition(2, 1, 'save / 1')]
                       }
        }
        self.RefDFA_G.initial_state = State(0)
        self.traces=[['open / 1', 'edit / 1', 'save / 1'],
                ['load / 1', 'open / 1', 'exit / 2'],
                ['load / 1', 'open / 1', 'edit / 1', 'save / 1'],
                ['load / 1', 'open / 1', 'edit / 1', 'save / 1', 'exit / 2']]

    def test_build_labeled_pta(self):
        pta = PTA()
        pta.build_labeled_pta(self.RefDFA_G, self.traces)
        pta.G.print_graph()

        expected_pta = Graph()
        expected_pta.graph = {
            State(0): {
                State(1): [Transition(State(0), State(1), "open / 1")],
                State(4): [Transition(State(0), State(4), "load / 1")]
            },
            State(1): {
                State(2): [Transition(State(1), State(2), "edit / 1")]
            },
            State(2): {
                State(3): [Transition(State(2), State(3), "save / 1")]
            },
            State(3): {},  # Leaf state
                State(4): {
                State(5): [Transition(State(4), State(5), "open / 1")]
            },
            State(5): {
                State(6): [Transition(State(5), State(6), "exit / 2")],
                State(7): [Transition(State(5), State(7), "edit / 1")]
            },
            State(6): {},  # Leaf state
                State(7): {
                State(8): [Transition(State(7), State(8), "save / 1")]
            },
            State(8): {
                State(9): [Transition(State(8), State(9), "exit / 2")]
            },
            State(9): {}  # Leaf state
        }
        expected_pta.initial_state = State(0)
        check_reference_states = True
        for state, transitions in pta.G.graph.items():
            if state.label in [0, 4, 6, 9] and state.get_reference_state() == State(0):
                print(f'{state.label}: true')
            elif state.label in [1, 5, 8] and state.get_reference_state() == State(1):
                print(f'{state.label}: true')
            elif state.label in [2, 7] and state.get_reference_state() == State(2):
                print(f'{state.label}: true')

        self.assertEqual(expected_pta, pta.G)  # add assertion here

    def test_returned_values(self):
        pta = PTA()
        inputs, outputs, alphabet = pta.build_labeled_pta(self.RefDFA_G, self.traces)
        v1 = inputs.sort() == ['edit', 'load', 'open', 'save', 'exit'].sort()
        v2 = outputs.sort() == ['1', '2'].sort()
        v3 = alphabet.sort() == ['edit / 1', 'load / 1', 'open / 1', 'save / 1', 'exit / 2'].sort()
        self.assertTrue(v1)
        self.assertTrue(v2)
        self.assertTrue(v3) # add assertion here
if __name__ == '__main__':
    unittest.main()

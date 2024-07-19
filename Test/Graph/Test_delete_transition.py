import unittest

from Graph import Graph
from State import State
from Transition import Transition


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.G = Graph()

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
        transition4 = Transition(state1, state2, 'b/1')
        transition5 = Transition(state1, state1, 'a/1')
        transition6 = Transition(state5, state6, 'b/1')
        self.G.graph = {
            state0: {state1: [transition1]},
            state1: {state2: [transition2, transition4], state1: [transition5]},
            state2: {state3: [transition3]},
            state3: {state4: [transition4]},
            state4: {},
            state5: {state6: [transition6]},
            state6: {}
        }

        self.G.initial_state = state0

    def test_something(self):
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
        transition4 = Transition(state1, state2, 'b/1')
        transition5 = Transition(state1, state1, 'a/1')
        transition6 = Transition(state5, state6, 'b/1')

        self.G.delete_Transition(transition4)

        new_G = Graph()
        new_G.graph = {
            state0: {state1: [transition1]},
            state1: {state2: [transition2], state1: [transition5]},
            state2: {state3: [transition3]},
            state3: {state4: [transition4]},
            state4: {},
            state5: {state6: [transition6]},
            state6: {}
        }

        new_G.initial_state = state0
        self.assertEqual(new_G, self.G)  # add assertion here


if __name__ == '__main__':
    unittest.main()

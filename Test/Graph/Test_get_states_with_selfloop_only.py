import unittest

from Graph import Graph
from State import State
from Transition import Transition


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.G = Graph()

        self.state0 = State(0)
        self.state1 = State(1)
        self.state2 = State(2)
        self.state3 = State(3)
        self.state4 = State(4)
        self.state5 = State(5)
        self.state6 = State(6)

        self.G.graph = {
            self.state0: {self.state1: [Transition(self.state0, self.state1, 'a/1')]},
            self.state1: {self.state2: [Transition(self.state1, self.state2, 'b/1')],
                          self.state1: [Transition(self.state1, self.state1, 'a/1')]},
            self.state2: {self.state3: [Transition(self.state2, self.state3, 'b/1')]},
            self.state3: {self.state3: [Transition(self.state3, self.state3, 'b/1')]},
            self.state4: {self.state3: [Transition(self.state4, self.state3, 'a/1')]},
            self.state5: {self.state6: [ Transition(self.state5, self.state6, 'b/1')]},
            self.state6: {}
        }
    def test_something(self):
        actual_resutl = self.G.get_states_with_selflopp_only()
        self.assertEqual([self.state3], actual_resutl)  # add assertion here


if __name__ == '__main__':
    unittest.main()

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

        self.transition1 = Transition(self.state0, self.state1, 'a/1')
        self.transition2 = Transition(self.state1, self.state2, 'a/2')
        self.transition3 = Transition(self.state2, self.state3, 'b/1')
        self.transition4 = Transition(self.state1, self.state2, 'b/1')
        self.transition5 = Transition(self.state1, self.state1, 'a/1')
        self.transition6 = Transition(self.state5, self.state6, 'b/1')
        self.transition7 = Transition(self.state3, self.state4, 'a/2')
        self.G.graph = {
            self.state0: {self.state1: [self.transition1]},
            self.state1: {self.state2: [self.transition2, self.transition4],
                          self.state1: [self.transition5]},
            self.state2: {self.state3: [self.transition3]},
            self.state3: {self.state4: [self.transition7]},
            self.state4: {},
            self.state5: {self.state6: [self.transition6]},
            self.state6: {}
        }
    def test_something(self):
        actual_result = self.G.get_all_transitons()
        expected_result = [self.transition1, self.transition2,
                           self.transition4, self.transition5,
                           self.transition3, self.transition7,
                           self.transition6]
        self.assertEqual(expected_result, actual_result)  # add assertion here

if __name__ == '__main__':
    unittest.main()

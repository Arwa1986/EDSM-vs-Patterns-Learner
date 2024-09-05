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

        self.state4.color = 'red'
        self.state0.color = 'red'
        self.state1.color = 'red'
        transition1 = Transition(self.state0, self.state1, 'a/1')
        transition2 = Transition(self.state1, self.state2, 'a/2')
        transition3 = Transition(self.state2, self.state3, 'b/1')
        transition4 = Transition(self.state1, self.state2, 'b/1')
        transition5 = Transition(self.state1, self.state1, 'a/1')
        transition6 = Transition(self.state5, self.state6, 'b/1')
        self.G.graph = {
            self.state0: {self.state1: [transition1]},
            self.state1: {self.state2: [transition2, transition4], self.state1: [transition5]},
            self.state2: {self.state3: [transition3]},
            self.state3: {self.state4: [transition4]},
            self.state4: {},
            self.state5: {self.state6: [transition6]},
            self.state6: {}
        }

        self.G.initial_state = self.state0

    def test_graph_wih_leaves(self):
        actual_result = self.G.get_leaves()

        self.assertEqual([self.state4, self.state6], actual_result)  # add assertion here

    def test_graph_with_no_leaves(self):
        transition7 = Transition(self.state4, self.state6, 'b/1')
        self.G.graph[self.state4] = {self.state6:[transition7]}

        transition8 = Transition(self.state6, self.state1, 'b/1')
        self.G.graph[self.state6] = {self.state1: [transition8]}
        actual_result = self.G.get_leaves()

        self.assertEqual([], actual_result)  # add assertion here


if __name__ == '__main__':
    unittest.main()

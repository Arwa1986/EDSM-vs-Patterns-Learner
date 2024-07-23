import unittest
from Graph import Graph
from State import State
from Transition import Transition

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.g = Graph()

        self.state0 = State('S0', 'accepted', True)
        self.state1 = State('S1', 'accepted', False)
        transition0 = Transition(self.state0, self.state1, 'A')
        transition1 = Transition(self.state0,self.state0, 'B')
        transition2 = Transition(self.state1, self.state0, 'C')

        self.g.graph = {self.state0: {self.state1: [transition0], self.state0: [transition1]}}
        self.g.graph[self.state1] = {self.state0: [transition2]}

    def test_set_initail_state_with_exiting_one(self):
        self.g.set_initial_state(self.state1)
        expected_result = self.state0
        self.assertEqual(expected_result, self.g.initial_state)

    def test_set_initail_state_with_the_same_exiting_one(self):
        self.g.set_initial_state(self.state0)
        expected_result = self.state0
        self.assertEqual(expected_result, self.g.initial_state)

if __name__ == "__main__":
    unittest.main()
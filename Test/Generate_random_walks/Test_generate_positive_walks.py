import unittest

from Apps.RandomWalksGenerator import generate_positive_walks
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
        self.transition5 = Transition(self.state1, self.state1, 'b/1')
        self.transition6 = Transition(self.state5, self.state6, 'b/1')
        self.transition7 = Transition(self.state3, self.state4, 'a/2')
        self.G.graph = {
            self.state0: {self.state1: [self.transition1],
                          self.state5: [Transition(self.state0, self.state5, 'b/2')]},

            self.state1: {self.state2: [self.transition2, self.transition4],
                          self.state1: [self.transition5]},

            self.state2: {self.state3: [self.transition3],
                          self.state6: [Transition(self.state2, self.state6, 'a/1')]},

            self.state3: {self.state4: [self.transition7],
                          self.state2: [Transition(self.state3, self.state2, 'a/2')]},

            self.state4: {self.state4: [Transition(self.state4, self.state4, 'b/2')],
                          self.state5: [Transition(self.state4, self.state5, 'a/1')]},

            self.state5: {self.state6: [self.transition6],
                          self.state0: [Transition(self.state5, self.state0, 'a/1')]},

            self.state6: {self.state1: [Transition(self.state6, self.state1, 'b/2')],
                          self.state2: [Transition(self.state6, self.state2, 'a/2')]}
        }
        self.G.set_initial_state(self.state0)
        self.G.set_input_alphabet(['a', 'b'])
        self.G.set_output_alphabet(['1', '2'])

    def test_generate_positive_walks(self):
        positive_walks_size = 10
        max_length = 5
        positive_walks = generate_positive_walks(positive_walks_size, max_length, self.G)

        positive_walk = True
        for walk in positive_walks:
            # def is_trace_in_G(self, trace):  # trace is a set of strings ['a','a', 'b', 'x']
                s = self.G.initial_state
                for label in positive_walks:
                    s = self.G.get_target_state_for_label(s, label)
                    if not s:
                        positive_walk = False
                        break
                if not positive_walk:
                    break
        self.assertEqual(True, positive_walk)  # add assertion here


if __name__ == '__main__':
    unittest.main()
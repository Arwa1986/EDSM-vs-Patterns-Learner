import unittest

import networkx as nx

from Graph import Graph
from State import State
from Utilities.Dictionary_Networkx_Converter import *

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.networkx_graph = nx.MultiDiGraph()
        self.networkx_graph.add_edge(0, 1, label='A')
        self.networkx_graph.add_edge(0, 2, label='B')
        self.networkx_graph.add_edge(2, 3, label='A')
        self.networkx_graph.add_edge(3, 1, label='B')
        self.networkx_graph.add_edge(1, 4, label='B')


    # def test_add_states(self):
    #     actual_graph = convert_states_networkx_to_dictionary(self.networkx_graph, )
    #     exp_dic = {State(0):{},
    #                       State(1):{},
    #                       State(2):{},
    #                       State(3):{},
    #                       State(4):{}}
    #     expected_graph = Graph()
    #     expected_graph.graph = exp_dic
    #     expected_graph.set_initial_state(State(0))
    #     result = (actual_graph == expected_graph)
    #     self.assertEqual(True, result)  # add assertion here
    #
    # def test_add_states2(self):
    #     actual_graph = convert_states_networkx_to_dictionary(self.networkx_graph)
    #     exp_dic = {State(0):{State(3):[]},
    #                       State(1):{},
    #                       State(2):{},
    #                       State(3):{},
    #                       State(4):{}}
    #     expected_graph = Graph()
    #     expected_graph.graph = exp_dic
    #     expected_graph.set_initial_state(State(0))
    #     result = (actual_graph == expected_graph)
    #     self.assertEqual(False, result)  # add assertion here

    def test_initial_state(self):
        actual_initial_state = find_initial_state(self.networkx_graph)
        self.assertEqual(State(0), actual_initial_state)

    def test_convert_networkx_to_dictionary(self):
        actual_graph = networkx_to_dictionary(self.networkx_graph)
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        state4 = State(4)
        exp_dic = {state0: {state1: [Transition(state0, state1, 'A')], state2: [Transition(state0, state2, 'B')]},
                   state1: {state4: [Transition(state1, state4, 'B')]},
                   state2: {state3: [Transition(state2, state3, 'A')]},
                   state3: {state1: [Transition(state3, state1, 'B')]},
                   state4: {}}
        expected_graph = Graph()
        expected_graph.graph = exp_dic
        expected_graph.set_initial_state(state0)
        result = (actual_graph == expected_graph)
        self.assertEqual(True, result)  # add assertion here

if __name__ == '__main__':
    unittest.main()

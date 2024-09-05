import unittest

from Graph import Graph
from State import State
from Utilities.Dictionary_Networkx_Converter import networkx_to_dictionary
from Utilities.DotFile_Networks_converter import dot_to_multidigraph
from Utilities.Pattern import sink_state_pattern


class MyTestCase(unittest.TestCase):

    def test_automata_with_sink_state(self):
        dot_path = 'coffeemachine.dot'  # Replace with your DOT file path
        multi_di_graph = dot_to_multidigraph(dot_path)
        Graph_obj = Graph()
        Graph_obj = networkx_to_dictionary(multi_di_graph)
        sink_states, output = sink_state_pattern(Graph_obj)

        self.assertEqual([State('s1')], sink_states)  # add assertion here
        self.assertEqual([' error'], output)  # add assertion here
if __name__ == '__main__':
    unittest.main()

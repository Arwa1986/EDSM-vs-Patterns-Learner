import unittest

from Patterns.extract_patterns_from_reference_DFA import get_all_input_sequences_with_one_output, get_combinations
from Patterns.output_for_input_sequence_pattern import Output_for_input_sequence_pattern
from State import State
from Utilities.Dictionary_Networkx_Converter import networkx_to_dictionary
from Utilities.DotFile_Networks_converter import dot_to_multidigraph
from Utilities.Pattern import get_actual_output_for_input_sequence


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # 1- dot to MultiDiGraph
        coffeMahchine_MultiDiGraph = dot_to_multidigraph('../coffeemachine.dot')

        # 2- MultiDiGraph to Graph (our object)
        self.coffeMachine_Graph = networkx_to_dictionary(coffeMahchine_MultiDiGraph)
        self.coffeMachine_Graph.set_initial_state(State('s0'))
        self.coffeMachine_Graph.set_input_alphabet(['WATER ', 'POD ', 'BUTTON ', 'CLEAN '])
        self.coffeMachine_Graph.set_output_alphabet([' ok', ' error', ' coffee!'])
    def test_get_actual_output_for_input_sequence(self):
        expect_output = ' error'
        actual_output = get_actual_output_for_input_sequence(['BUTTON ', 'WATER '], self.coffeMachine_Graph, self.coffeMachine_Graph.get_all_states())
        self.assertEqual(expect_output, actual_output)  # add assertion here

    def test_get_actual_output_for_input_sequence2(self):
        expect_output = ' error'
        actual_output = get_actual_output_for_input_sequence(['CLEAN ', 'BUTTON '], self.coffeMachine_Graph, self.coffeMachine_Graph.get_all_states())
        self.assertEqual(expect_output, actual_output)  # add assertion here

    def test_get_all_input_sequences_with_only_output(self):
        output_pattern_list = sorted(get_all_input_sequences_with_one_output(self.coffeMachine_Graph, 2))
        expected_list = sorted([Output_for_input_sequence_pattern(('BUTTON ', 'BUTTON '), ' error'),
                                Output_for_input_sequence_pattern(('BUTTON ', 'WATER '), ' error'),
                                Output_for_input_sequence_pattern(('CLEAN ', 'BUTTON '), ' error'),
                                Output_for_input_sequence_pattern(('BUTTON ', 'POD '), ' error')
                                ])

        self.assertEqual(True, output_pattern_list == expected_list)  # add assertion here

    def test_get_all_combainations_of_input_sequences(self):
        combination_list = sorted(get_combinations(self.coffeMachine_Graph.input_alphabet, 2))
        expected_list = sorted([('WATER ', 'WATER '), ('WATER ', 'POD '), ('WATER ', 'BUTTON '), ('WATER ', 'CLEAN '),
                                ('POD ', 'WATER '), ('POD ', 'POD '), ('POD ', 'BUTTON '), ('POD ', 'CLEAN '),
                                ('BUTTON ', 'WATER '), ('BUTTON ', 'POD '), ('BUTTON ', 'BUTTON '), ('BUTTON ', 'CLEAN '),
                                ('CLEAN ', 'WATER '), ('CLEAN ', 'POD '), ('CLEAN ', 'BUTTON '), ('CLEAN ', 'CLEAN ')
                                ])

        self.assertEqual(True, combination_list == expected_list)


if __name__ == '__main__':
    unittest.main()

import unittest

from Form_Converters.GraphObj_DotFile_converter import dot_to_Graph
from Patterns.extract_patterns_from_reference_DFA import extract_patterns_for_group1, check_for_violations


class MyTestCase(unittest.TestCase):
    def setUp(self):
        graph_obj = dot_to_Graph('coffeemachine.dot')
        patterns = extract_patterns_for_group1(graph_obj)
        print(f'number of patterns: {len(patterns)}')
        violated_patterns = check_for_violations(graph_obj, patterns)
        print(f'number of violated patterns: {len(violated_patterns)}')

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()

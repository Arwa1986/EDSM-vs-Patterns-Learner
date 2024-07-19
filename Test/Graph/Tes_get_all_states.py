import unittest

from State import State
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):
        positive_traces = [['a/1', 'a/2', 'b/1', 'b/1'], ['a/1', 'a/1', 'b/1'], ['a/1', 'a/2', 'b/1', 'a/1']]
        self.pta = PTA()
        self.pta.build_pta(positive_traces)
    def test_something(self):
        result = self.pta.G.get_all_states()

        expected_result = [State(0), State(1), State(2), State(3), State(4), State(5), State(6), State(7)]
        self.assertEqual(expected_result,result)  # add assertion here



if __name__ == '__main__':
    unittest.main()

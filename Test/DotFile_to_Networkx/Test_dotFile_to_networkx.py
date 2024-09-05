import unittest

from Utilities.DotFile_Networks_converter import dot_to_multidigraph


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # Example usage:
        dot_path = 'coffeemachine.dot'  # Replace with your DOT file path
        multi_di_graph = dot_to_multidigraph(dot_path)

        actual_edges = list(multi_di_graph.edges(data=True))
        expected_edges = [('__start0', 's0', {}),
                          ('s0', 's0', {'label': 'CLEAN / ok'}),
                          ('s0', 's1', {'label': 'BUTTON / error'}),
                          ('s0', 's2', {'label': 'POD / ok'}),
                          ('s0', 's4', {'label': 'WATER / ok'}),
                          ('s1', 's1', {'label': 'WATER / error'}),
                          ('s1', 's1', {'label': 'POD / error'}),
                          ('s1', 's1', {'label': 'BUTTON / error'}),
                          ('s1', 's1', {'label': 'CLEAN / error'}),
                          ('s2', 's0', {'label': 'CLEAN / ok'}),
                          ('s2', 's1', {'label': 'BUTTON / error'}),
                          ('s2', 's2', {'label': 'POD / ok'}),
                          ('s2', 's3', {'label': 'WATER / ok'}),
                          ('s3', 's0', {'label': 'CLEAN / ok'}),
                          ('s3', 's3', {'label': 'WATER / ok'}),
                          ('s3', 's3', {'label': 'POD / ok'}),
                          ('s3', 's5', {'label': 'BUTTON / coffee!'}),
                          ('s4', 's0', {'label': 'CLEAN / ok'}),
                          ('s4', 's1', {'label': 'BUTTON / error'}),
                          ('s4', 's3', {'label': 'POD / ok'}),
                          ('s4', 's4', {'label': 'WATER / ok'}),
                          ('s5', 's0', {'label': 'CLEAN / ok'}),
                          ('s5', 's1', {'label': 'WATER / error'}),
                          ('s5', 's1', {'label': 'POD / error'}),
                          ('s5', 's1', {'label': 'BUTTON / error'})]

        self.assertEqual(expected_edges, actual_edges)  # add assertion here


if __name__ == '__main__':
    unittest.main()

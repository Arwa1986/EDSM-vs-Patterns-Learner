import unittest
from Patterns.Mariani_Pattern import get_ifXenevntuallyY_patterns
from Utilities.PTA import PTA

class TestGetMarianiPatterns(unittest.TestCase):

    def test_valid_input(self):
        traces = [['open / 1', 'edit / 1', 'save / 1', 'exit / 2'],
                  ['open / 1', 'edit / 1', 'edit / 1']]
        pta = PTA()
        pta.build_pta(traces)
        patterns = sorted(get_ifXenevntuallyY_patterns(pta))
        expected_patterns = sorted([
            'LTLSPEC G ((! (input=open & output=1)) | F((input=open & output=1)) & F (input=edit & output=1)))',
            'LTLSPEC G ((! (input=open & output=1)) | F((input=open & output=1)) & F (input=save & output=1)))',
            'LTLSPEC G ((! (input=open & output=1)) | F((input=open & output=1)) & F (input=exit & output=2)))',
            'LTLSPEC G ((! (input=edit & output=1)) | F((input=edit & output=1)) & F (input=open & output=1)))',
            'LTLSPEC G ((! (input=edit & output=1)) | F((input=edit & output=1)) & F (input=save & output=1)))',
            'LTLSPEC G ((! (input=edit & output=1)) | F((input=edit & output=1)) & F (input=exit & output=2)))',
            'LTLSPEC G ((! (input=save & output=1)) | F((input=save & output=1)) & F (input=open & output=1)))',
            'LTLSPEC G ((! (input=save & output=1)) | F((input=save & output=1)) & F (input=edit & output=1)))',
            'LTLSPEC G ((! (input=save & output=1)) | F((input=save & output=1)) & F (input=exit & output=2)))',
            'LTLSPEC G ((! (input=exit & output=2)) | F((input=exit & output=2)) & F (input=open & output=1)))',
            'LTLSPEC G ((! (input=exit & output=2)) | F((input=exit & output=2)) & F (input=edit & output=1)))',
            'LTLSPEC G ((! (input=exit & output=2)) | F((input=exit & output=2)) & F (input=save & output=1)))'
        ])
        self.assertEqual(patterns, expected_patterns)

    def test_empty_input(self):
        pta = PTA()
        pta.build_pta([])
        patterns = get_ifXenevntuallyY_patterns(pta)
        self.assertEqual(patterns, [])

if __name__ == '__main__':
    unittest.main()
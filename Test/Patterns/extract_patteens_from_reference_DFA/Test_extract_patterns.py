import unittest

from Patterns.extract_patterns_from_reference_DFA import get_group1_patterns


class MyTestCase(unittest.TestCase):
    def test_extract_patterns_for_one_event_one_event_scope(self):
        group1_patterns = sorted(get_group1_patterns(['water', 'ok'], [['pod', 'ok'], ['water', 'error']]))

        expected_result = sorted([
                           'LTLSPEC F (input = water & output = ok) -> (!(input = water & output = ok) U (input = pod & output = ok))',
                           'LTLSPEC F (input = water & output = ok) -> (!(input = water & output = ok) U (input = water & output = error))',
                           'LTLSPEC G((input = pod & output = ok) -> G(!(input = water & output = ok)))',
                           'LTLSPEC G((input = water & output = error) -> G(!(input = water & output = ok)))',
                           'LTLSPEC !(input = pod & output = ok) W ((input = water & output = ok) & !(input = pod & output = ok))',
                           'LTLSPEC !(input = water & output = error) W ((input = water & output = ok) & !(input = water & output = error))',
                           'LTLSPEC G (!(input = pod & output = ok)) | F ((input = pod & output = ok) & F (input = water & output = ok)))',
                           'LTLSPEC G (!(input = water & output = error)) | F ((input = water & output = error) & F (input = water & output = ok)))',
                           'LTLSPEC F (input = pod & output = ok) -> ((input = water & output = ok) U (input = pod & output = ok))',
                           'LTLSPEC F (input = water & output = error) -> ((input = water & output = ok) U (input = water & output = error))',
                           'LTLSPEC G ((input = pod & output = ok) -> G((input = water & output = ok)))',
                           'LTLSPEC G ((input = water & output = error) -> G((input = water & output = ok)))'])

        self.assertEqual(True, group1_patterns == expected_result)  # add assertion here

if __name__ == '__main__':
    unittest.main()

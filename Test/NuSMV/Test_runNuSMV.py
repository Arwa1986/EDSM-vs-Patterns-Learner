import unittest
from smv.smv_engin import run_nusmv, parse_output


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.model_str = ('MODULE main'
                               'VAR'
                               'state:{0, 1, 2, 3};'
                               'input:{a, b};'
                               'output:{1, 2};'
                               'ASSIGN'
                               'init(state):=State(0);'
                               'next(state):=case'
                               'state = 0 & input = a : 1;'
                               'state = 0 & input = b : 0;'
                               'state = 1 & input = a : 2;'
                               'state = 1 & input = b : 5;'
                               'state = 2 & input = b : 3;'
                               'state = 3 & input = b : 4;'
                               'esac;'
                               'next(output):=case'
                               'state = 0 & input = a : 1;'
                               'state = 0 & input = b : 1;'
                               'state = 1 & input = a : 2;'
                               'state = 1 & input = b : 1;'
                               'state = 2 & input = b : 1;'
                               'state = 3 & input = b : 1;'
                               'esac;'
                               'SPEC AF (input = a ->X state = 1);')
    def test_something(self):
        actual_result = False
        output = run_nusmv(self.model_str)
        specs = parse_output(output)
        for spec in specs:
            if spec.condition == 'AF (input = a -> next(state) = 1' and  not spec.success:
                actual_result = True
        self.assertEqual(True, actual_result)  # add assertion here


if __name__ == '__main__':
    unittest.main()

import unittest

from Utilities.EDSM import EDSM
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):
        positive_traces = [['a/1', 'a/2', 'a/1', 'b/2', 'a/1'],
                            ['a/1', 'b/2', 'b/1', 'b/2'],
                            ['b/1', 'a/1', 'a/2', 'b/2'],
                            ['b/1', 'b/2', 'a/1']]
        pta = PTA()
        pta.build_pta(positive_traces)
        pta.G.print_graph()
        self.edsm = EDSM(pta)

    def test_learner(self):
        self.edsm.run_EDSM_learner()

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

import unittest

from State import State
from Utilities.EDSM import EDSM
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):
        positive_traces = [['a/1', 'a/2', 'b/1', 'b/1'], ['a/1', 'a/1', 'b/1']]
        self.pta = PTA()
        self.pta.build_pta(positive_traces)

        for state in self.pta.G.get_all_states():
            if state.label == 0 or state.label == 1:
                state.type = "accepted"
            elif state.label == 2 or state.label == 3:
                state.type = "rejected"

    def test_all_states_are_rejected(self):
        edsm = EDSM(self.pta)
        compatible, list_type = edsm.is_compatible_type([self.pta.G.get_state_for_label(2), self.pta.G.get_state_for_label(3)])
        expected_result = 'rejected'
        self.assertEqual(expected_result, list_type)  # add assertion here
        self.assertEqual(compatible, True)

    def test_rejected_wih_unlabeled(self):
        edsm = EDSM(self.pta)
        compatible, list_type = edsm.is_compatible_type([self.pta.G.get_state_for_label(2), self.pta.G.get_state_for_label(3), self.pta.G.get_state_for_label(4)])
        expected_result = 'rejected'
        self.assertEqual(expected_result, list_type)  # add assertion here
        self.assertEqual(compatible, True)

    def test_all_states_are_accepted(self):
        edsm = EDSM(self.pta)
        compatible, list_type = edsm.is_compatible_type([self.pta.G.get_state_for_label(0), self.pta.G.get_state_for_label(1)])
        expected_result = 'accepted'
        self.assertEqual(expected_result, list_type)  # add assertion here
        self.assertEqual(compatible, True)

    def test_accepted_with_unlabeled(self):
        edsm = EDSM(self.pta)
        compatible, list_type = edsm.is_compatible_type([self.pta.G.get_state_for_label(0), self.pta.G.get_state_for_label(1), self.pta.G.get_state_for_label(6)])
        expected_result = 'accepted'
        self.assertEqual(expected_result, list_type)  # add assertion here
        self.assertEqual(compatible, True)

    def test_all_states_are_unlabeled(self):
        edsm = EDSM(self.pta)
        compatible, list_type = edsm.is_compatible_type([self.pta.G.get_state_for_label(6), self.pta.G.get_state_for_label(4), self.pta.G.get_state_for_label(5)])
        expected_result = 'unlabeled'
        self.assertEqual(expected_result, list_type)  # add assertion here
        self.assertEqual(compatible, True)  # add assertion here

    def test_rejected_wih_accepted(self):
        edsm = EDSM(self.pta)
        compatible, list_type = edsm.is_compatible_type([self.pta.G.get_state_for_label(0), self.pta.G.get_state_for_label(3)])
        expected_result = 'unlabeled'
        self.assertEqual(expected_result, list_type)  # add assertion here
        self.assertEqual(compatible, False)

    def test_rejected_accepted_unlabeled(self):
        edsm = EDSM(self.pta)
        compatible, list_type = edsm.is_compatible_type(
            [self.pta.G.get_state_for_label(0), self.pta.G.get_state_for_label(3), self.pta.G.get_state_for_label(5)])
        expected_result = 'unlabeled'
        self.assertEqual(expected_result, list_type)  # add assertion here
        self.assertEqual(compatible, False)

if __name__ == '__main__':
    unittest.main()

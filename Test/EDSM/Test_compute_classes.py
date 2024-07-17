import unittest

from State import State
from Transition import Transition
from Utilities.DISJOINTSETS import DisjointSet
from Utilities.EDSM import EDSM
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.state1 = State(1)
        self.state3 = State(3)
        self.state6 = State(6)
        self.state7 = State(7)
        self.state8 = State(8)

        transition1 = Transition(self.state1, self.state6, 'A')
        transition2 = Transition(self.state1, self.state6, 'B')
        transition3 = Transition(self.state1, self.state6, 'C')
        transition4 = Transition(self.state6, self.state3, 'C')
        transition5 = Transition(self.state6, self.state7, 'B')
        transition6 = Transition(self.state7, self.state1, 'A')
        transition7 = Transition(self.state7, self.state8, 'C')
        graph ={
            self.state1: {self.state6: [transition2, transition3]},
            self.state6: {self.state3: [transition4]},
            self.state7: { self.state8: [transition7]}
        }

        self.pta = PTA()
        self.pta.G.initial_state = self.state1
        self.pta.G.graph = graph

    def test_something(self):
        edsm = EDSM(self.pta)
        edsm.red_states = [self.state1, self.state3, self.state6, self.state8]
        ds = DisjointSet()
        ds.s1 = self.state1
        ds.s2 = self.state7
        edsm.make_set_for_every_state_rooted_at(ds, self.state1)
        edsm.make_set_for_every_state_rooted_at(ds, self.state7)
        work_to_do = {}
        add_new_state = ds.union(self.state1, self.state7)
        work_to_do[ds.find(self.state1)] = ds.get_set(self.state1)
        if add_new_state:
            edsm.compute_classes2(ds, work_to_do)

        expected_result = {self.state1: [self.state1, self.state7],
                           self.state3: [self.state3],
                           self.state6: [self.state6, self.state8]
                           }
        self.assertEqual(expected_result, ds.get_sets())  # add assertion here


if __name__ == '__main__':
    unittest.main()

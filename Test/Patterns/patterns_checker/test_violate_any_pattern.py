import unittest

from State import State
from Transition import Transition
from Utilities.Dictionary_Networkx_Converter import networkx_to_dictionary
from Utilities.DotFile_Networks_converter import dot_to_multidigraph
from Utilities.Learner import Learner
from Utilities.PTA import PTA


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # 1- dot to MultiDiGraph
        coffeMahchine_MultiDiGraph = dot_to_multidigraph('../coffeemachine.dot')

        # 2- MultiDiGraph to Graph (our object)
        self.coffeMachine_Graph = networkx_to_dictionary(coffeMahchine_MultiDiGraph)
        self.coffeMachine_Graph.set_initial_state(State('s0'))
        self.coffeMachine_Graph.set_input_alphabet(['WATER ', 'POD ', 'BUTTON ', 'CLEAN '])
        self.coffeMachine_Graph.set_output_alphabet([' ok', ' error', ' coffee!'])
    def test_something(self):
        CM_partial_pta = PTA()
        s0 = State('s0')
        s1 = State('s1')
        s2 = State('s2')
        s3 = State('s3')
        s4 = State('s4')
        s5 = State('s5')
        s12 = State('s12')
        s13 = State('s13')
        s41 = State('s41')
        s31 = State('s31')
        s15 = State('s15')
        s16 = State('s16')
        s17 = State('s17')
        s18 = State('s18')

        CM_partial_pta.G.graph = {s0: {
            s0: [Transition(s0, s0, 'CLEAN / ok')],
            s2: [Transition(s0, s2, 'POD / ok')],
            s4: [Transition(s0, s4, 'WATER / ok')],
            s1: [Transition(s0, s1, 'BUTTON / error')]
        },
            s1: {
                s12: [Transition(s1, s12, 'BUTTON / error')],
            },
            s2: {
                s3: [Transition(s2, s3, 'WATER / ok')],
                s1: [Transition(s2, s1, 'BUTTON / error')],
                s0: [Transition(s2, s0, 'CLEAN / ok')],
            },
            s3: {
                s3: [Transition(s3, s3, 'WATER / ok'),
                     Transition(s3, s3, 'POD / ok')],
                s5: [Transition(s3, s5, 'BUTTON / coffee!')],
            },
            s4: {
                s0: [Transition(s4, s0, 'CLEAN / ok')],
                s31: [Transition(s4, s31, 'POD / ok')],
                s41: [Transition(s4, s41, 'WATER / ok')],
                s1: [Transition(s4, s1, 'BUTTON / error')]
            },
            s5: {
                s15: [Transition(s5, s15, 'WATER / error')],
                s17: [Transition(s5, s17, 'BUTTON / error')],
            },
            s12: {
                s13: [Transition(s12, s13, 'WATER / error')]
            },
            s13: {},
            s41: {},
            s31: {},
            s15: {
                s16: [Transition(s17, s16, 'POD / error')],
            },
            s16: {},
            s17: {
                s18: [Transition(s17, s18, 'WATER / error')],
            },
            s18: {}
        }

        edsmPattern = Learner(CM_partial_pta)
        edsmPattern.red_states = [s0, s1, s2, s3, s4]
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

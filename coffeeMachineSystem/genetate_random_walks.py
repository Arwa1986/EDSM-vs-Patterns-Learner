from Apps.RandomWalksGenerator import generate_random_walks
from State import State
from Utilities.Dictionary_Networkx_Converter import networkx_to_dictionary
from Utilities.DotFile_Networks_converter import dot_to_multidigraph
from Utilities.Draw_graph import draw_multiDigraph
from Utilities.EDSM import EDSM
from Utilities.PTA import PTA

# convert dot file to Graph

# 1- dot to MultiDiGraph
coffeMahchine_MultiDiGraph = dot_to_multidigraph('coffeemachine.dot')

# Draw the original system:
# draw_multiDigraph(coffeMahchine_MultiDiGraph, '../coffeeMachineSystem/coffeemachine_reference')
#
# 2- MultiDiGraph to Graph (our object)
coffeMachine_Graph = networkx_to_dictionary(coffeMahchine_MultiDiGraph)
coffeMachine_Graph.set_initial_state(State('s0'))
coffeMachine_Graph.set_input_alphabet(['WATER ', 'POD ', 'BUTTON ', 'CLEAN '])
coffeMachine_Graph.set_output_alphabet([' ok', ' error', ' coffee!'])

# 3- generate random walks
coffeMachine_positive_walks = generate_random_walks(coffeMachine_Graph, 10, 50)

for walk in coffeMachine_positive_walks:
    print(walk)
# # 4- build PTA
# coffeMachine_pta = PTA()
# coffeMachine_pta.build_pta(coffeMachine_positive_walks)
#
# # run EDSM learner
# coffeMachine_edsm = EDSM(coffeMachine_pta)
# coffeMachine_edsm.run_EDSM_learner()


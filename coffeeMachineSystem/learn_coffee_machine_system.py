from Apps.RandomWalksGenerator import generate_random_walks
from State import State
from Utilities.Dictionary_Networkx_Converter import networkx_to_dictionary
from Utilities.DotFile_Networks_converter import dot_to_multidigraph
from Utilities.Draw_graph import draw_multiDigraph, draw_multidigraph_with_labels
from Utilities.EDSM import EDSM
from Utilities.PTA import PTA
from Utilities.evaluation import Evaluation

# convert dot file to Graph

# 1- dot to MultiDiGraph
coffeMahchine_MultiDiGraph = dot_to_multidigraph('coffeemachine.dot')

# Draw the original system:
# draw_multiDigraph(coffeMahchine_MultiDiGraph, '../coffeeMachineSystem/coffeemachine_reference')
draw_multidigraph_with_labels(coffeMahchine_MultiDiGraph, '../coffeeMachineSystem/coffeemachine_reference')

# 2- MultiDiGraph to Graph (our object)
coffeMachine_Graph = networkx_to_dictionary(coffeMahchine_MultiDiGraph)
coffeMachine_Graph.set_initial_state(State('s0'))
coffeMachine_Graph.set_input_alphabet(['WATER ', 'POD ', 'BUTTON ', 'CLEAN '])
coffeMachine_Graph.set_output_alphabet([' ok', ' error', ' coffee!'])

# 3- generate random walks
coffeMachine_positive_walks, coffeMachine_negative_walks = generate_random_walks(coffeMachine_Graph, 10, 80, 30)
# split the positive traces into traning and evaluation traces
evaluation_CM_positive_walks=[]
for i in range(len(coffeMachine_positive_walks)-50):
      # evaluation traces
      evaluation_CM_positive_walks.append(coffeMachine_positive_walks[i])
      # remove the evaluation traces
      coffeMachine_positive_walks.remove(coffeMachine_positive_walks[i])

print('__________Learning______________')
print('__________Positive Traces_________')
for walk in coffeMachine_positive_walks:
    print(walk)
# 4- build PTA
coffeMachine_pta = PTA()
coffeMachine_pta.build_pta(coffeMachine_positive_walks)

# run EDSM learner
coffeMachine_edsm = EDSM(coffeMachine_pta)
coffeMachine_edsm.run_EDSM_learner()

# evaluate the learned automata
print('__________EVALUATION______________')
print('__________Positive Traces_________')
for walk in coffeMachine_positive_walks:
    print(walk)
print('__________Negative Traces_________')
for walk in coffeMachine_negative_walks:
    print(walk)

e = Evaluation(coffeMachine_edsm, evaluation_CM_positive_walks, coffeMachine_negative_walks)
true_positive, true_negative, false_positive, false_negative, precision, recall, specificity, F_measure, Accuracy, BCR = e.evaluate()
print(f'true_positive = {true_positive}\n'
      f'true_negative = {true_negative}\n,'
      f'false_positive = {false_positive}\n,'
      f'false_negative = {false_negative}\n,'
      f'precision = {precision}\n,'
      f'recall = {recall}\n,'
      f'specificity = {specificity}\n,'
      f'F_measure = {F_measure}\n,'
      f'Accuracy = {Accuracy}\n,'
      f'BCR = {BCR}\n')

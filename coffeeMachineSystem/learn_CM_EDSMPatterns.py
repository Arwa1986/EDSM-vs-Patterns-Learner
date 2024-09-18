# convert dot file to Graph
from Apps.RandomWalksGenerator import generate_random_walks
from Patterns.extract_patterns_from_reference_DFA import get_all_input_sequences_with_one_output
from State import State
from Utilities.Dictionary_Networkx_Converter import networkx_to_dictionary
from Utilities.DotFile_Networks_converter import dot_to_multidigraph
from Utilities.Draw_graph import draw_multidigraph_with_labels
from Utilities.Learner import Learner
from Utilities.PTA import PTA
from Utilities.evaluation import Evaluation

# 1- dot to MultiDiGraph
coffeMahchine_MultiDiGraph = dot_to_multidigraph('coffeemachine.dot')

# Draw the original system:
# draw_multiDigraph(coffeMahchine_MultiDiGraph, '../coffeeMachineSystem/coffeemachine_reference')
# draw_multidigraph_with_labels(coffeMahchine_MultiDiGraph, '../coffeeMachineSystem/coffeemachine_reference')

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

# 4- Extract Patterns from Reference DFA
patterns_list = get_all_input_sequences_with_one_output(coffeMachine_Graph, 2)
for p in patterns_list:
    p.print()

# 5- build PTA
coffeMachine_pta = PTA()
input_list, output_list = coffeMachine_pta.build_pta(coffeMachine_positive_walks)
coffeMachine_pta.G.set_input_alphabet(input_list)
coffeMachine_pta.G.set_output_alphabet(output_list)
#
# print(f'INPUT: {coffeMachine_pta.G.get_input_alphabet()}')
# print(f'OUTPUT: {coffeMachine_pta.G.get_output_alphabet()}')
# run EDSM learner
coffeMachine_edsmPattens = Learner(coffeMachine_pta)
coffeMachine_edsmPattens.setup()
coffeMachine_edsmPattens.run_EDSM_with_pattern_learner(patterns_list)


# evaluate the learned automata
# print('__________EVALUATION______________')
# print('__________Positive Traces_________')
# for walk in coffeMachine_positive_walks:
#     print(walk)
# print('__________Negative Traces_________')
# for walk in coffeMachine_negative_walks:
#     print(walk)

e = Evaluation(coffeMachine_edsmPattens, evaluation_CM_positive_walks, coffeMachine_negative_walks)
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


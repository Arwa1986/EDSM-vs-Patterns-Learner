# convert dot file to Graph
import copy

import pexpect

from Apps.RandomWalksGenerator import generate_random_walks
from Form_Converters.GraphObj_DotFile_converter import dot_to_Graph
from Patterns.extract_patterns_from_reference_DFA import get_negative_patterns
from Utilities.Learner import Learner
from Utilities.PTA import PTA
from Utilities.evaluation import Evaluation
from Utilities.write_clear_file import clear_file
from smv.smv_engin import close_nusmv

clear_file('EDSM_Learner_tracker.txt')
clear_file('EDSM+Patterns_Learner_tracker.txt')
# 1- dot to Dictionary
TE_Graph = dot_to_Graph('TextEditor.dot')

# 2- generate random walks
Training_TE_pos_walks, evalutation_TE_neg_walks = generate_random_walks(TE_Graph, 5, 30, 10)
# split the positive traces into traning and evaluation traces
evaluation_TE_pos_walks=[]
for i in range(len(Training_TE_pos_walks) - 20):
      # evaluation traces
      evaluation_TE_pos_walks.append(Training_TE_pos_walks[i])
      # remove the evaluation traces
      Training_TE_pos_walks.remove(Training_TE_pos_walks[i])
#
# print('__________Learning______________')
# print('__________Positive Traces_________')
# for walk in Training_TE_pos_walks:
#     print(f'{walk},')
Training_TE_pos_walks = [
['load / 1', 'open / 1'],
['save / 0', 'edit / 0'],
['load / 1', 'load / 1', 'edit / 0'],
['save / 0', 'save / 0', 'open / 0', 'save / 0'],
['exit / 0', 'open / 0', 'edit / 0', 'open / 0', 'open / 0'],
['open / 1', 'save / 0', 'open / 0', 'open / 0'],
['edit / 0'],
['edit / 0', 'open / 0', 'exit / 0', 'edit / 0', 'save / 0'],
['open / 1', 'open / 0', 'save / 0', 'load / 0'],
['open / 1', 'edit / 1', 'exit / 0'],
['load / 1', 'load / 1', 'open / 1'],
['open / 1'],
['edit / 0', 'save / 0', 'load / 0', 'open / 0', 'edit / 0'],
['save / 0', 'open / 0', 'open / 0', 'exit / 0'],
['edit / 0', 'edit / 0', 'exit / 0', 'load / 0', 'exit / 0'],
['open / 1', 'open / 0', 'save / 0', 'edit / 0', 'exit / 0'],
['save / 0'],
['load / 1', 'open / 1', 'edit / 1'],
['save / 0', 'open / 0', 'save / 0'],
['save / 0', 'open / 0'],
['open / 1', 'edit / 1', 'save / 1', 'exit / 2'],
]

#
# Training_TE_pos_walks = [
# ['edit / 0'],
# ['load / 1', 'exit / 0'],
# ['save / 0', 'save / 0', 'load / 0', 'load / 0', 'exit / 0'],
# ['load / 1', 'save / 0', 'exit / 0', 'edit / 0'],
# ['load / 1'],
# ['open / 1', 'load / 0', 'save / 0'],
# ['load / 1', 'load / 1', 'exit / 0', 'load / 0', 'exit / 0'],
# ['open / 1', 'exit / 2', 'open / 1'],
# ['open / 1', 'edit / 1', 'load / 0'],
# ['exit / 0'],
# ['load / 1', 'save / 0', 'edit / 0', 'open / 0', 'edit / 0'],
# ['edit / 0', 'save / 0'],
# ['save / 0'],
# ['edit / 0', 'edit / 0', 'load / 0', 'open / 0', 'exit / 0'],
# ['edit / 0', 'exit / 0', 'load / 0', 'exit / 0'],
# ['save / 0', 'edit / 0', 'exit / 0'],
# ['edit / 0', 'load / 0'],
# ['exit / 0', 'exit / 0'],
# ['open / 1', 'edit / 1', 'save / 1', 'open / 0'],
# ['save / 0', 'edit / 0'],
# ]
# 3- build PTA
TE_pta = PTA()
input_list, output_list = TE_pta.build_labeled_pta(TE_Graph, Training_TE_pos_walks)
TE_pta.G.set_input_alphabet(input_list)
TE_pta.G.set_output_alphabet(output_list)

TE_pta_copy = copy.deepcopy(TE_pta)

# 4- run EDSM learner
TE_edsm= Learner(TE_pta)
TE_edsm.setup()

TE_edsm.run_EDSM_learner()

# 5- Evaluate the learned automata
print('~~~~~~~~~~~~ EDSM ~~~~~~~~~~~~')
e = Evaluation(TE_edsm, evaluation_TE_pos_walks, evalutation_TE_neg_walks)
true_positive, true_negative, false_positive, false_negative, precision, recall, specificity, F_measure, Accuracy, BCR = e.evaluate()
print(f'true_positive = {true_positive}\n'
      f'true_negative = {true_negative}\n'
      f'false_positive = {false_positive}\n'
      f'false_negative = {false_negative}\n'
      f'precision = {precision}\n'
      f'recall = {recall}\n'
      f'specificity = {specificity}\n'
      f'F_measure = {F_measure}\n'
      f'Accuracy = {Accuracy}\n'
      f'BCR = {BCR}\n')
# ============================================================
# ============================================================
#  Run EDSM+Patterns

# 1- delete any transition that has an error output
TE_Graph_without_sink_state = dot_to_Graph('TextEditor_no_sink_state.dot')

# 2- Extract Patterns from Reference DFA
negative_patterns_list = get_negative_patterns(TE_Graph_without_sink_state)
print(f'number of negative patterns = {len(negative_patterns_list)}')

# 3- build PTA
# PTA already built in the previous step

# 4- run EDSM+patterns learner
TE_edsmPattens = Learner(TE_pta_copy)
TE_edsmPattens.setup()

TE_edsmPattens.run_EDSM_with_pattern_learner(negative_patterns_list)
print(f'number of merges: {TE_edsmPattens.counter}')
# close_nusmv()

print('~~~~~~~~~ EDSM+PATTERNS ~~~~~~~~~')
e = Evaluation(TE_edsmPattens, evaluation_TE_pos_walks, evalutation_TE_neg_walks)
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
#

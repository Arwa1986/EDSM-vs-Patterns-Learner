# convert dot file to Graph
import copy

from lazr.restfulclient.resource import missing

from Apps.RandomWalksGenerator import generate_Training_positive_walks, \
      generate_prefixed_closed_negative_walks, generate_evaluation_positive_walks
from Form_Converters.GraphObj_DotFile_converter import dot_to_Graph
from Patterns.Mariani_Pattern import get_safety_patterns
from Utilities.Learner import Learner
from Utilities.PTA import PTA
from Utilities.evaluation import Evaluation
from Utilities.write_clear_file import clear_file


edsm_file_name = 'EDSM_Learner_tracker.txt'
with_patterns_file_name = 'Mariani_Learner_tracker.txt'
clear_file(edsm_file_name)
clear_file(with_patterns_file_name)

# 1- dot to Dictionary
TE_Graph = dot_to_Graph('TextEditor.dot')

# 1-1 find the ture properties
temp_pta = PTA()
temp_pta.G = TE_Graph
true_safety_properties = get_safety_patterns(temp_pta)


print('------ Generating Random Walks ------')
# 2- generate random walks
# positive walks with states and transitions coverage
Training_TE_pos_walks = generate_Training_positive_walks(10, 10, TE_Graph)

# Evaluation walks: positive and negative walks
evaluation_TE_pos_walks = generate_evaluation_positive_walks(5, 6, TE_Graph)
evalutation_TE_neg_walks = generate_prefixed_closed_negative_walks(5, 6, TE_Graph)

print('__________Positive Traces_________')
for walk in Training_TE_pos_walks:
    print(f'{walk},')
# Training_TE_pos_walks = [
# ['load / 1', 'open / 1'],
# ['save / 0', 'edit / 0'],
# ['load / 1', 'load / 1', 'edit / 0'],
# ['save / 0', 'save / 0', 'open / 0', 'save / 0'],
# ['exit / 0', 'open / 0', 'edit / 0', 'open / 0', 'open / 0'],
# ['open / 1', 'save / 0', 'open / 0', 'open / 0'],
# ['edit / 0'],
# ['edit / 0', 'open / 0', 'exit / 0', 'edit / 0', 'save / 0'],
# ['open / 1', 'open / 0', 'save / 0', 'load / 0'],
# ['open / 1', 'edit / 1', 'exit / 0'],
# ['load / 1', 'load / 1', 'open / 1'],
# ['open / 1'],
# ['edit / 0', 'save / 0', 'load / 0', 'open / 0', 'edit / 0'],
# ['save / 0', 'open / 0', 'open / 0', 'exit / 0'],
# ['edit / 0', 'edit / 0', 'exit / 0', 'load / 0', 'exit / 0'],
# ['open / 1', 'open / 0', 'save / 0', 'edit / 0', 'exit / 0'],
# ['save / 0'],
# ['load / 1', 'open / 1', 'edit / 1'],
# ['save / 0', 'open / 0', 'save / 0'],
# ['save / 0', 'open / 0'],
# ['open / 1', 'edit / 1', 'save / 1', 'exit / 2'],
# ]

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
print('============ EDSM ============')
# 4- run EDSM learner
TE_edsm= Learner(TE_pta)
TE_edsm.setup(edsm_file_name, with_patterns_file_name)

TE_edsm.run_EDSM_learner()

# 5- Evaluate the learned automata
print('~~~~~~~~~~~~ EVALUATION:EDSM ~~~~~~~~~~~~')
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
#  Run Mariani
# Mariani: we extract patterns from the PTA using NuSMV
# patterns are in the form of if x then eventually y
# positive patterns are the one with 100% confidence
# during the merging process, positive patterns must never be violated
print('============With Patterns============')
# 1- build PTA
# PTA already built in the previous step

# print('__________ Safety Patterns form reference automata _________')
# for p in true_safety_properties:
#     print(p)

# 2- get positive patterns
patterns = get_safety_patterns(TE_pta_copy)
# print('__________ Safety Patterns form traces _________')
# for p in patterns:
#     print(p)

#  compare the two sets of patterns
missing_counter = 0
found_counter = 0
for rp in true_safety_properties:
    if rp not in patterns:
        # print(f'pattern {rp} is missing')
        missing_counter += 1
    else:
        # print(f'pattern {rp} is found')
        found_counter += 1
print(f'found patterns: {found_counter}, missing patterns: {missing_counter}')
print(f'proportion of correctly specified patterns: {round(found_counter/len(patterns),2)*100}%')


# 4- run EDSM+patterns learner
TE_edsmPattens = Learner(TE_pta_copy)
TE_edsmPattens.setup(edsm_file_name, with_patterns_file_name)

TE_edsmPattens.run_EDSM_with_pattern_learner(patterns)
# print(f'number of merges: {TE_edsmPattens.counter}')
# close_nusmv()

print('~~~~~~~~~ EVALUATION: EDSM+PATTERNS ~~~~~~~~~')
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

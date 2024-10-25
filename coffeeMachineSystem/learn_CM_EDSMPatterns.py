# convert dot file to Graph
import pexpect

from Apps.RandomWalksGenerator import generate_random_walks
from Form_Converters.GraphObj_DotFile_converter import dot_to_Graph
from Patterns.extract_patterns_from_reference_DFA import get_negative_patterns
from Utilities.Learner import Learner
from Utilities.PTA import PTA
from Utilities.evaluation import Evaluation
from smv.smv_engin import close_nusmv

# 1- dot to Dictionary
# CM_Graph = dot_to_Graph('coffeemachine.dot')

# 3- generate random walks
# Training_CM_pos_walks, evalutation_CM_neg_walks = generate_random_walks(CM_Graph, 10, 80, 30)
# split the positive traces into traning and evaluation traces
# evaluation_CM_pos_walks=[]
# for i in range(len(Training_CM_pos_walks) - 50):
#       # evaluation traces
#       evaluation_CM_pos_walks.append(Training_CM_pos_walks[i])
#       # remove the evaluation traces
#       Training_CM_pos_walks.remove(Training_CM_pos_walks[i])
#
# print('__________Learning______________')
# print('__________Positive Traces_________')
# for walk in Training_CM_pos_walks:
#     print(f'{walk},')

# 3- delete any transition that has an error output
CM_Graph_without_error_output = dot_to_Graph('coffeemachine_without_error.dot')
# 4- Extract Patterns from Reference DFA
negative_patterns_list = get_negative_patterns(CM_Graph_without_error_output)
print(f'number of negative patterns = {len(negative_patterns_list)}')
print('__________Negative Patterns_________')
for p in negative_patterns_list:
    print(p)
print('------------ Learning Process started ------------')

Training_CM_pos_walks = [['WATER / ok'],
['POD / ok', 'POD / ok', 'BUTTON / error', 'WATER / error', 'CLEAN / error', 'BUTTON / error', 'BUTTON / error', 'CLEAN / error', 'WATER / error'],
['WATER / ok', 'CLEAN / ok', 'POD / ok', 'CLEAN / ok', 'WATER / ok'],
['BUTTON / error', 'BUTTON / error'],
['CLEAN / ok', 'BUTTON / error', 'CLEAN / error', 'CLEAN / error', 'WATER / error', 'POD / error'],
['CLEAN / ok', 'POD / ok'],
['WATER / ok', 'WATER / ok', 'BUTTON / error', 'BUTTON / error'],
['BUTTON / error', 'WATER / error', 'BUTTON / error'],
['BUTTON / error'],
['POD / ok', 'BUTTON / error', 'POD / error'],
['POD / ok', 'POD / ok', 'BUTTON / error', 'WATER / error', 'BUTTON / error'],
['CLEAN / ok'],
['WATER / ok', 'WATER / ok', 'POD / ok', 'WATER / ok', 'BUTTON / coffee', 'WATER / error', 'WATER / error'],
['BUTTON / error', 'WATER / error', 'BUTTON / error', 'WATER / error', 'BUTTON / error', 'CLEAN / error', 'CLEAN / error', 'BUTTON / error', 'WATER / error', 'CLEAN / error'],
['WATER / ok', 'CLEAN / ok', 'POD / ok', 'WATER / ok', 'CLEAN / ok'],
['POD / ok', 'CLEAN / ok', 'CLEAN / ok', 'POD / ok'],
['BUTTON / error', 'POD / error', 'POD / error', 'BUTTON / error', 'WATER / error'],
['WATER / ok', 'BUTTON / error', 'WATER / error'],
['BUTTON / error', 'BUTTON / error', 'POD / error', 'WATER / error', 'WATER / error', 'BUTTON / error', 'WATER / error'],
['CLEAN / ok', 'POD / ok', 'CLEAN / ok'],
['POD / ok', 'WATER / ok', 'WATER / ok', 'CLEAN / ok', 'WATER / ok', 'BUTTON / error', 'POD / error'],
['WATER / ok', 'WATER / ok', 'CLEAN / ok', 'CLEAN / ok', 'BUTTON / error', 'POD / error', 'CLEAN / error'],
['POD / ok', 'CLEAN / ok', 'BUTTON / error', 'WATER / error', 'POD / error', 'WATER / error'],
['CLEAN / ok', 'CLEAN / ok', 'BUTTON / error', 'POD / error', 'CLEAN / error', 'CLEAN / error', 'BUTTON / error', 'CLEAN / error'],
['BUTTON / error', 'CLEAN / error', 'WATER / error', 'BUTTON / error', 'WATER / error', 'CLEAN / error', 'POD / error', 'BUTTON / error'],
['BUTTON / error', 'BUTTON / error', 'CLEAN / error', 'CLEAN / error', 'POD / error', 'WATER / error', 'CLEAN / error'],
['BUTTON / error', 'CLEAN / error', 'WATER / error', 'CLEAN / error', 'CLEAN / error'],
['WATER / ok', 'BUTTON / error', 'WATER / error', 'WATER / error', 'BUTTON / error'],
['POD / ok', 'BUTTON / error', 'BUTTON / error', 'BUTTON / error', 'CLEAN / error', 'CLEAN / error'],
['BUTTON / error', 'WATER / error', 'WATER / error', 'CLEAN / error', 'WATER / error', 'POD / error', 'BUTTON / error', 'CLEAN / error', 'BUTTON / error', 'WATER / error'],
['WATER / ok', 'POD / ok', 'CLEAN / ok', 'WATER / ok', 'BUTTON / error', 'BUTTON / error', 'CLEAN / error', 'POD / error', 'POD / error', 'POD / error'],
['POD / ok', 'CLEAN / ok', 'BUTTON / error'],
['WATER / ok', 'WATER / ok', 'CLEAN / ok', 'BUTTON / error', 'CLEAN / error', 'POD / error', 'BUTTON / error', 'WATER / error', 'BUTTON / error'],
['BUTTON / error', 'POD / error', 'WATER / error', 'POD / error', 'WATER / error', 'CLEAN / error', 'WATER / error', 'POD / error', 'BUTTON / error', 'POD / error'],
['CLEAN / ok', 'CLEAN / ok', 'WATER / ok', 'CLEAN / ok'],
['WATER / ok', 'BUTTON / error', 'WATER / error', 'BUTTON / error', 'BUTTON / error', 'CLEAN / error', 'POD / error', 'BUTTON / error', 'POD / error', 'CLEAN / error'],
['POD / ok', 'CLEAN / ok', 'WATER / ok', 'POD / ok', 'POD / ok'],
['POD / ok', 'BUTTON / error', 'POD / error', 'BUTTON / error', 'BUTTON / error', 'POD / error', 'POD / error', 'POD / error'],
['POD / ok', 'CLEAN / ok', 'BUTTON / error', 'CLEAN / error', 'CLEAN / error', 'WATER / error'],
['CLEAN / ok', 'WATER / ok', 'POD / ok', 'POD / ok'],
['BUTTON / error', 'BUTTON / error', 'CLEAN / error', 'POD / error'],
['POD / ok', 'BUTTON / error', 'BUTTON / error', 'CLEAN / error'],
['WATER / ok', 'WATER / ok', 'BUTTON / error', 'POD / error'],
['BUTTON / error', 'WATER / error'],
['POD / ok', 'CLEAN / ok', 'BUTTON / error', 'WATER / error', 'BUTTON / error', 'POD / error', 'CLEAN / error', 'BUTTON / error', 'POD / error'],
['WATER / ok', 'BUTTON / error', 'WATER / error', 'POD / error', 'WATER / error'],
['POD / ok', 'WATER / ok', 'POD / ok', 'WATER / ok', 'WATER / ok', 'CLEAN / ok', 'POD / ok', 'WATER / ok', 'CLEAN / ok', 'CLEAN / ok'],
['CLEAN / ok', 'WATER / ok', 'WATER / ok', 'POD / ok', 'WATER / ok', 'CLEAN / ok', 'BUTTON / error', 'POD / error', 'CLEAN / error', 'POD / error'],
['POD / ok', 'POD / ok', 'WATER / ok', 'WATER / ok', 'BUTTON / coffee', 'WATER / error', 'WATER / error', 'WATER / error'],
['BUTTON / error', 'CLEAN / error', 'POD / error']]

# 5- build PTA
coffeMachine_pta = PTA()
input_list, output_list = coffeMachine_pta.build_pta(Training_CM_pos_walks)
coffeMachine_pta.G.set_input_alphabet(input_list)
coffeMachine_pta.G.set_output_alphabet(output_list)

# run EDSM learner
coffeMachine_edsmPattens = Learner(coffeMachine_pta)
coffeMachine_edsmPattens.setup()

coffeMachine_edsmPattens.run_EDSM_with_pattern_learner(negative_patterns_list)
close_nusmv()
#
# e = Evaluation(coffeMachine_edsmPattens, evaluation_CM_pos_walks, evalutation_CM_neg_walks)
# true_positive, true_negative, false_positive, false_negative, precision, recall, specificity, F_measure, Accuracy, BCR = e.evaluate()
# print(f'true_positive = {true_positive}\n'
#       f'true_negative = {true_negative}\n,'
#       f'false_positive = {false_positive}\n,'
#       f'false_negative = {false_negative}\n,'
#       f'precision = {precision}\n,'
#       f'recall = {recall}\n,'
#       f'specificity = {specificity}\n,'
#       f'F_measure = {F_measure}\n,'
#       f'Accuracy = {Accuracy}\n,'
#       f'BCR = {BCR}\n')
#

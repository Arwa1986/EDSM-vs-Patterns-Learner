# convert dot file to Graph
import pexpect

from Apps.RandomWalksGenerator import generate_random_walks
from Form_Converters.GraphObj_DotFile_converter import dot_to_Graph
from Patterns.extract_patterns_from_reference_DFA import get_negative_patterns
from Utilities.Learner import Learner
from Utilities.PTA import PTA
from Utilities.evaluation import Evaluation

# 1- dot to Dictionary
CM_Graph = dot_to_Graph('coffeemachine.dot')

# 3- generate random walks
Training_CM_pos_walks, evalutation_CM_neg_walks = generate_random_walks(CM_Graph, 10, 80, 30)
# split the positive traces into traning and evaluation traces
evaluation_CM_pos_walks=[]
for i in range(len(Training_CM_pos_walks) - 50):
      # evaluation traces
      evaluation_CM_pos_walks.append(Training_CM_pos_walks[i])
      # remove the evaluation traces
      Training_CM_pos_walks.remove(Training_CM_pos_walks[i])

# print('__________Learning______________')
# print('__________Positive Traces_________')
# for walk in coffeMachine_positive_walks:
#     print(walk)

# 4- Extract Patterns from Reference DFA
negative_patterns_list = get_negative_patterns(CM_Graph)
print(f'number of negative patterns = {len(negative_patterns_list)}')
# patterns_list = get_all_input_sequences_with_one_output(coffeMachine_Graph, 2)
# for p in patterns_list:
#     p.print()


# 5- build PTA
coffeMachine_pta = PTA()
input_list, output_list = coffeMachine_pta.build_pta(Training_CM_pos_walks)
coffeMachine_pta.G.set_input_alphabet(input_list)
coffeMachine_pta.G.set_output_alphabet(output_list)

# run EDSM learner
coffeMachine_edsmPattens = Learner(coffeMachine_pta)
coffeMachine_edsmPattens.setup()


with pexpect.spawn("/home/arwa/Programs/NuSMV-2.6.0-linux64/NuSMV-2.6.0-Linux/bin/NuSMV -int") as smv:
      smv.expect("NuSMV >")  # Wait for a prompt
      coffeMachine_edsmPattens.run_EDSM_with_pattern_learner(negative_patterns_list)


# evaluate the learned automata
# print('__________EVALUATION______________')
# print('__________Positive Traces_________')
# for walk in coffeMachine_positive_walks:
#     print(walk)
# print('__________Negative Traces_________')
# for walk in coffeMachine_negative_walks:
#     print(walk)

e = Evaluation(coffeMachine_edsmPattens, evaluation_CM_pos_walks, evalutation_CM_neg_walks)
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


from Apps.RandomWalksGenerator import generate_random_walks, split_into_evaluation_and_training_lists
from Form_Converters.GraphObj_DotFile_converter import dot_to_Graph
# from State import State
# from Form_Converters.Dictionary_Networkx_Converter import networkx_to_dictionary
# from Form_Converters.DotFile_Networks_converter import dot_to_multidigraph
from Utilities.Learner import Learner
from Utilities.PTA import PTA
from Utilities.evaluation import Evaluation
from Utilities.write_clear_file import write_to_file_in_new_line, clear_file

# clear files:
clear_file('EDSM_Learner_Traces')
clear_file('EDSM_Learner_tracker.txt')

## 1- dot to Dictionary
CM_Graph = dot_to_Graph('coffeemachine.dot')

# 3- generate random walks
CM_pos_walks, evalutation_CM_neg_walks = generate_random_walks(CM_Graph, 10, 80, 30)
# split the positive traces into training and evaluation traces
Evaluation_CM_pos_walks, Training_CM_pos_walks= split_into_evaluation_and_training_lists(CM_pos_walks)

write_to_file_in_new_line('EDSM_Learner_Traces', '__________Learning______________')
write_to_file_in_new_line('EDSM_Learner_Traces', '__________Positive Traces_________')
for walk in Training_CM_pos_walks:
      walk_str = ''
      for label in walk:
            walk_str+=label
            walk_str+=', '
      write_to_file_in_new_line('EDSM_Learner_Traces', walk_str)
# 4- build PTA
coffeMachine_pta = PTA()
coffeMachine_pta.build_pta(Training_CM_pos_walks)

# run EDSM learner
coffeMachine_edsm = Learner(coffeMachine_pta)
coffeMachine_edsm.setup('EDSM_Learner_tracker.txt', 'EDSM_PAT_Learner_tracker.txt')
print('-------PTA--------')
coffeMachine_edsm.pta.G.print_graph()
coffeMachine_edsm.run_EDSM_learner()

# evaluate the learned automata
write_to_file_in_new_line('EDSM_Learner_Traces', '__________EVALUATION______________')
write_to_file_in_new_line('EDSM_Learner_Traces', '__________Positive Traces_________')
for walk in Evaluation_CM_pos_walks:
      walk_str = ''
      for label in walk:
            walk_str += label
            walk_str += ', '
      write_to_file_in_new_line('EDSM_Learner_Traces', walk_str)
write_to_file_in_new_line('EDSM_Learner_Traces', '__________Negative Traces_________')
for walk in evalutation_CM_neg_walks:
      walk_str = ''
      for label in walk:
            walk_str += label
            walk_str += ', '
      write_to_file_in_new_line('EDSM_Learner_Traces', walk_str)

e = Evaluation(coffeMachine_edsm, Evaluation_CM_pos_walks, evalutation_CM_neg_walks)
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
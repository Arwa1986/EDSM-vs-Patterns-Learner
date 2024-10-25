# 3- delete any transition that has an error output
from Form_Converters.GraphObj_DotFile_converter import dot_to_Graph
from Patterns.extract_patterns_from_reference_DFA import get_negative_patterns

CM_Graph_without_error_output = dot_to_Graph('coffeeMachineSystem/coffeemachine_without_error.dot')
# 4- Extract Patterns from Reference DFA
negative_patterns_list = get_negative_patterns(CM_Graph_without_error_output)
print(f'number of negative patterns = {len(negative_patterns_list)}')
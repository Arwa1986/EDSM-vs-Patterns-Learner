import itertools

from Patterns.output_for_input_sequence_pattern import Output_for_input_sequence_pattern
from Utilities.Pattern import get_actual_output_for_input_sequence


def get_all_input_sequences_with_one_output(graph, sequence_length):
    # get all input sequences for fixed length
    combinations = get_combinations(graph.input_alphabet, sequence_length)
    patterns = []
    for seq in combinations:
        output  = get_actual_output_for_input_sequence(seq, graph, graph.get_all_states())
        if output:
            new_pattern = Output_for_input_sequence_pattern(seq, output)
            patterns.append(new_pattern)

    return patterns

def get_combinations(input_list, length):
    # Use itertools.product to get all combinations of the specified length
    return list(itertools.product(input_list, repeat=length))
import itertools

import pexpect

from smv.smv_engin import check_nusmv_model, parse_output, run_nusmv
from Patterns.list_of_patterns import design_group1_patterns
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



def extract_patterns_for_group1(graph):
    # get all transitions from the reference automata: set of all transitions
    patterns = []
    labels_set = graph.get_transitions_labels_set()
    for label in labels_set:
        temp = get_group1_patterns(label, labels_set)
        for p in temp:
            patterns.append(p)
    return patterns

# make set of input/output pairs
# match the input/output pairs with the patterns
def get_group1_patterns(event, labels):
    patterns = []
    for R in labels:
        temp = design_group1_patterns(event, R)
        for p in temp:
            patterns.append(p)
    return patterns

    # patterns_violate_reference_graph = check_for_violations (graph, patterns)

def check_for_violations (graph, patterns):
    graph_SMV = graph.to_nusmv(graph.get_all_states(), patterns)

    output, err = run_nusmv(graph_SMV)
    specs = parse_output(output, err)
    # print_output(specs)

    patterns_violate_reference_graph = []
    for p in specs:
        if not p.success:
            patterns_violate_reference_graph.append(p.condition)
    return patterns_violate_reference_graph

def get_negative_patterns(graph):
    group1_patterns = extract_patterns_for_group1(graph)
    negative_patterns_list = check_for_violations(graph, group1_patterns)
    return negative_patterns_list

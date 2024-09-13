from Patterns.output_for_input_sequence_pattern import Output_for_input_sequence_pattern


def violate_any_pattern(patterns, G):
    violate = False
    for pattern in patterns:
       if isinstance(pattern, Output_for_input_sequence_pattern):
           if pattern.violated_by_partial_graph(G):
               violate = True

    return violate
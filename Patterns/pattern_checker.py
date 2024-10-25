from Patterns.output_for_input_sequence_pattern import Output_for_input_sequence_pattern
# from smv.main import output
from smv.smv_engin import run_nusmv, check_nusmv_model, parse_output


def violate_any_pattern(patterns, G, red_states):
    violate = False
    for pattern in patterns:
       if isinstance(pattern, Output_for_input_sequence_pattern):
           if pattern.violated_by_partial_graph(G, red_states):
               violate = True

    return violate

def violate_any_pattern2(patterns, G):# G is the graph object
    violate = False
    G_nusmv_str = G.to_nusmv(patterns)
    # output,errors = check_nusmv_model(G_nusmv_str)
    output, errors = run_nusmv(G_nusmv_str)
    checked_patterns = parse_output(output, errors)

    violated_patterns = []
    for spec in checked_patterns:
       if not spec.success:
            violate = True
            violated_patterns.append(spec)
    return violate, violated_patterns
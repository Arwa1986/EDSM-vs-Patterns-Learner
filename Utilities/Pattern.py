from Graph import Graph
from Utilities.EDSM import EDSM


def sink_state_pattern(graph:Graph):
    found = False
    sink_states = []
    # leaves = graph.get_leaves()
    # if leaves:
    #     for leaf in leaves:
    #         incoming_transitions = graph.get_incoming_transitions(leaf)
    #         output_set = set()
    #         for in_tran in incoming_transitions:
    #             output_set.add(in_tran.output)
    #         if len(output_set) == 1:
    #             found = True
    #             sink_states.append(leaf)
    for s in graph.get_states_with_selflopp_only():
        sink_states.append(s)
    for s in sink_states:
        incoming_edges = graph.get_incoming_transitions(s)
        # find the output that leads to the sink state
        output = set()
        for t in incoming_edges:
            # exclude selfloop
            if t.from_state == s:
                continue
            output.add(t.output)

    return sink_states, list(output)

# this pattern returns the states that can be identified by
# an input/output pair 'transition label'
def identify_state_by_incoming_label_pattern(graph:Graph):
    identifiable_states = []

    all_transitions = graph.get_all_transitons()
    transitions_dic = {}
    for transition in all_transitions:
        if transition.label not in transitions_dic:
            transitions_dic[transition.label] = [transition.to_state]
        else:
            transitions_dic[transition.label].append(transition.to_state)

    for tran_label, target_states in transitions_dic.items():
        # remove any doublicate in the list of states
        target_states = set(target_states)
        target_states = list(target_states)
        if len(target_states) == 1:
            identifiable_states.append((target_states[0], tran_label))

    return identifiable_states

# if there are more than one red label that have incoming transition that identify a state
# then the partial graph violate the pattern
def violate_identify_state_by_incoming_label_pattern(partial_graph:EDSM, identifiable_states):
    violate_states = []
    red_states = partial_graph.red_states
    label_dict = {}
    for item in identifiable_states:
        label_dict[item[1]] = []
    for red in red_states:
        incoming_transitions = partial_graph.pta.G.get_incoming_transitions(red)
        for t in incoming_transitions:
            if t.label in label_dict:
                label_dict[t.label].append(t.to_state)

    for label, target_states in label_dict.items():
        target_states = set(target_states)
        target_states = list(target_states)
        if len(target_states) > 1:
            violate_states.append((target_states, label))
    return violate_states
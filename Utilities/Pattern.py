from Graph import Graph
# from Utilities.Learner import Learner

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
def violate_identify_state_by_incoming_label_pattern(partial_graph, identifiable_states): #partial_graph: Learner
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

def response_pattern(graph:Graph, event_p, event_s):
    found_event_p = False
    current_state = graph.initial_state
    state_with_event_p = dfs_find_states(graph, current_state, event_p)
    if state_with_event_p:
        current_state = graph.get_target_state(state_with_event_p, event_p)
        state_with_event_s = dfs_find_states(graph, current_state, event_s)

        all_outgoing_transitions = graph.get_outgoing_transitions_for_state(current_state)
        for transition in all_outgoing_transitions:
            if transition.label == event_s:
                found_event_p = True

# def depth_first_search(visited, state, graph:Graph, event_p, state_with_event_p):
#     # Mark the current vertex as visited
#     visited.append(state)
#     outgoing_transitions = graph.get_outgoing_transitions_for_state(state)
#     for t in outgoing_transitions:
#         if t.label == event_p:
#             state_with_event_p =  state
#     # Print the current vertex
#     # print(state, end=" ")
#
#     # Recursively visit all adjacent vertices
#     # that are not visited yet
#     for s in graph.get_children(state):
#         if s not in visited:
#             depth_first_search(visited, s, graph, event_p, state_with_event_p)
def dfs_find_states(graph, start_state, target_label):
    # Stack for DFS
    stack = [start_state]
    # Set to track visited states
    visited = set()
    # List to store states with the target label in outgoing transitions
    result_states = None
    found = False
    while stack or not found:
        # Pop the current state from the stack
        current_state = stack.pop()

        # Skip if the state has already been visited
        if current_state in visited:
            continue

        # Mark the current state as visited
        visited.add(current_state)

        # Check the outgoing transitions of the current state
        for next_state, transitions in graph.graph.get(current_state, {}).items():
            # Check each transition for the target label
            for transition in transitions:
                if transition.label == target_label:
                    result_states = current_state
                    found = True
                    break  # Stop checking other transitions if one is found

            # Add the next state to the stack for DFS traversal
            stack.append(next_state)
            if found:
                break

    return result_states

def get_actual_output_for_input_sequence(input_sequence, graph:Graph, states_of_interest):
    expected_output = None
    for state in states_of_interest:
        current_state = state
        for i in range(len(input_sequence)-1):
            current_state = graph.get_target_state(current_state, input_sequence[i])
        output = graph.get_output(current_state, input_sequence[-1])
        if not expected_output:
            expected_output = output
        elif output != expected_output:
            expected_output = None
            return expected_output

    return expected_output

# def violate_expected_output_for_input_sequence(all_inputSequebce_output_pairs, graph:Graph):
#     violate = False
#     for pair in all_inputSequebce_output_pairs:
#         input_sequence = pair[0]
#         expected_output = pair[1]
#         actual_output = expected_output_for_a_sequence_of_input(input_sequence, graph)
#         if actual_output != expected_output:
#             print(f' the last merge violates pattern: Expected_output_for_input_sequence')
#             print(f'This sequence of input should have {expected_output} as the only output')
#             violate = True
#
#     return violate

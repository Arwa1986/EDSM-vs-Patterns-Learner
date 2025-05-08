import random
from copy import copy

from Graph import Graph
from State import State
from Transition import Transition


def generate_random_walks(graph:Graph, max_length, positive_walks_size, negative_walks_size):
    positive_walks = generate_Training_positive_walks_sink_state_is_rejected(positive_walks_size, max_length, graph)
    negative_walks = generate_prefixed_closed_negative_walks_sink_state_is_rejected(negative_walks_size, max_length, graph)

    return positive_walks, negative_walks

def genetare_transition_cover_walks(graph, max_length, positive_walks_size):
    positive_walks = []
    i = 0
    all_states = graph.get_all_states()
    all_transitions = set(graph.get_outgoing_transitions_for_list_of_states(None, all_states))
    discovered_transitions = set()
    loop_counter = 0
    while discovered_transitions != all_transitions:
        loop_counter += 1
        # walk_length = random.randint(1, max_length)
        walk_length = max_length
        walk = []
        current_state = graph.initial_state
        for j in range(walk_length):
            input = random.choice(graph.input_alphabet)
            transition = graph.get_outgoing_transitions_for_state_with_input(current_state, input)
            walk.append(transition.label)
            if transition not in discovered_transitions:
                discovered_transitions.add(transition)
                break
            current_state = graph.get_target_state(current_state, input)
        if walk not in positive_walks:
            positive_walks.append(walk)
            i += 1
    print(f'loop counter: {loop_counter}')
    return positive_walks

def generate_Training_positive_walks(positive_walks_size, max_length, graph):
    positive_walks = []
    i = 0
    transition_cover = False
    state_cover = False
    all_states = graph.get_all_states()
    all_transitions = set(graph.get_outgoing_transitions_for_list_of_states(None, all_states))
    discovered_transitions = set()
    # discovered_states = []
    loop_counter = 0
    while i < positive_walks_size or (discovered_transitions!=all_transitions):
        loop_counter += 1
        walk_length = random.randint(1, max_length)
        walk = []
        current_state = graph.initial_state
        for j in range(walk_length):
            # if current_state not in discovered_states:
            #     discovered_states.append(current_state)
            input = random.choice(graph.input_alphabet)
            transition = graph.get_outgoing_transitions_for_state_with_input(current_state, input)
            # output = graph.get_output(current_state, input)
            # transition = input + ' / ' + output
            walk.append(transition.label)
            if transition not in discovered_transitions:
                discovered_transitions.add(transition)
            # if discovered_transitions == all_transitions:
            #     transition_cover = True
            # if discovered_states == all_states:
            #     state_cover = True
            current_state = graph.get_target_state(current_state, input)
        if walk not in positive_walks:
            positive_walks.append(walk)
            i += 1
    print(f'loop counter: {loop_counter}')
    return positive_walks
# def generate_Training_positive_walks(positive_walks_size, max_length, graph):
def generate_evaluation_positive_walks(positive_walks_size, max_length, graph):
    # positive walks that are not neccessarily cover all transitions and states
    positive_walks = []
    i = 0
    while i < positive_walks_size :
        walk_length = random.randint(1, max_length)
        walk = []
        current_state = graph.initial_state
        for j in range(walk_length):
            input = random.choice(graph.input_alphabet)
            transition = graph.get_outgoing_transitions_for_state_with_input(current_state, input)
            walk.append(transition.label)
            current_state = graph.get_target_state(current_state, input)
        if walk not in positive_walks:
            positive_walks.append(walk)
            i += 1
    return positive_walks

def generate_prefixed_closed_negative_walks(negative_walks_size, max_length, graph):
    negative_walks = []
    i = 0
    while i < negative_walks_size:
        walk_length = random.randint(1, max_length)
        walk = []
        current_state = graph.initial_state
        for j in range(walk_length - 1):
            input = random.choice(graph.input_alphabet)
            output = graph.get_output(current_state, input)
            transition = input + ' / ' + output
            walk.append(transition)
            current_state = graph.get_target_state(current_state, input)
        # generate the last transition that makes the walk negative. (add not exsitiing transition to the walk)
        input = random.choice(graph.input_alphabet)
        output = get_not_exist_output(current_state, input, graph)
        transition = input + '/' + output
        walk.append(transition)

        if walk not in negative_walks:
            negative_walks.append(walk)
            i += 1

    return negative_walks

def get_not_exist_output(state, input, graph):
    actual_output = graph.get_output(state, input)
    output_list_exclude_actual_output = [output for output in graph.output_alphabet if output != actual_output]

    random_not_exist_output = random.choice(output_list_exclude_actual_output)
    return random_not_exist_output

def long_enough():
    random_float = random.uniform(0, 1)
    return random_float == 0.7

def split_into_evaluation_and_training_lists(walks):
    Evaluation_pos_walks = []
    random_index_list = []
    for i in range(29):
        random_index = random.randint(0, len(walks) - 1)
        if random_index not in random_index_list:
            random_index_list.append(random_index)
            # add the evaluation traces
            Evaluation_pos_walks.append(walks[random_index])

    Training_pos_walks = []
    for i in range(len(walks) - 1):
        # remove the evaluation traces
        if i not in random_index_list:
            Training_pos_walks.append(walks[i])

    return Evaluation_pos_walks,Training_pos_walks

def generate_Training_positive_walks_sink_state_is_rejected(positive_walks_size, max_length, graph):
    positive_walks = []
    i = 0
    # transition_cover = False
    # state_cover = False
    # all_states = graph.get_all_states()
    # all_transitions = set(graph.get_outgoing_transitions_for_list_of_states(None, all_states))
    # discovered_transitions = set()
    # discovered_states = []
    loop_counter = 0
    while i < positive_walks_size :#or (discovered_transitions!=all_transitions)
        loop_counter += 1
        walk_length = random.randint(1, max_length)
        walk = []
        current_state = graph.initial_state
        while len(walk) < walk_length:
            input = random.choice(graph.input_alphabet)
            transition = graph.get_outgoing_transitions_for_state_with_input(current_state, input)
            if transition.to_state.color == 'yellow': # sink state
                continue
            walk.append(transition.label)
            # if transition not in discovered_transitions:
            #     discovered_transitions.add(transition)
            current_state = graph.get_target_state(current_state, input)
            # j+=1
        if walk not in positive_walks:
            positive_walks.append(walk)
            i += 1
    print(f'loop counter: {loop_counter}')
    return positive_walks

def generate_prefixed_closed_negative_walks_sink_state_is_rejected(negative_walks_size, max_length, graph):
    negative_walks = []
    i = 0
    while i < negative_walks_size:
        walk_length = random.randint(1, max_length)
        walk = []
        current_state = graph.initial_state
        for j in range(walk_length - 1):
            input = random.choice(graph.input_alphabet)
            # output = graph.get_output(current_state, input)
            # transition = input + ' / ' + output
            # walk.append(transition)
            transition = graph.get_outgoing_transitions_for_state_with_input(current_state, input)
            if transition.to_state.color == 'yellow':  # sink state
                continue
            walk.append(transition.label)
            current_state = graph.get_target_state(current_state, input)
        # generate the last transition that makes the walk negative. (add not exsitiing transition to the walk)
        input = random.choice(graph.input_alphabet)
        transition = graph.get_outgoing_transitions_for_state_with_input(current_state, input)
        if transition.to_state.color == 'yellow':  # sink state
            last_label = transition.label
        else:
            output = get_not_exist_output(current_state, input, graph)
            last_label = input + '/' + output
        walk.append(last_label)

        if walk not in negative_walks:
            negative_walks.append(walk)
            i += 1

    return negative_walks

if __name__ == '__main__':
    # Create the state objects
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)

    # Create the graph representation
    graph = {
        state0: {
            state0: [Transition(state0, state0, "b / 2")],
            state1: [Transition(state0, state1, "a / 1")]
        },
        state1: {
            state0: [Transition(state1, state0, "a / 1")],
            state2: [Transition(state1, state2, "b / 1")]
        },
        state2: {
            state1: [Transition(state2, state1, "b / 1")],
            state2: [Transition(state2, state2, "a / 2")]
        }
    }

    # Create the graph object
    G = Graph()
    G.graph = graph
    G.set_initial_state(state0)
    G.set_input_alphabet(['a', 'b'])
    G.set_output_alphabet(['1', '2'])

    positive_walks = generate_Training_positive_walks(5, 5, G)
    for walk in positive_walks:
        print(walk)
    print('=======================')
    positive_walks = genetare_transition_cover_walks(G, 5, 5)
    for walk in positive_walks:
        print(walk)
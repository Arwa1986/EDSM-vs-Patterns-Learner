import random

from Graph import Graph
from State import State
from Transition import Transition


def generate_random_walks(graph:Graph, alphabet, max_length, positive_walks_size, negative_walks_size):
    if max_length % 2 != 0:
        max_length += 1
    positive_walks = generate_positive_walks(positive_walks_size, max_length, graph, alphabet)
    # negative_walks = generate_prefixed_closed_negative_walks(negative_walks_size, max_length, graph)

def generate_positive_walks(size, max_length, graph, alphabet):
    positive_walks = []; i=0
    while i < size:
        current_state = graph.initial_state
        walk_length = random.randrange(2, max_length + 1, 2)
        walk = []; j=0
        while j < walk_length:
            transition_label = random.choice(alphabet)
            if graph.has_outgoing_transition_for_label(current_state, transition_label):
                walk.append(transition_label)
                current_state = graph.get_target_state_for_label(current_state, transition_label)
                j+=1

        if walk not in positive_walks:
            positive_walks.append(walk)
            i += 1
    return positive_walks


def generate_negative_walks(size, max_length, graph, alphabet):
    negative_walks = []; i=0
    while i < size:
        current_state = graph.initial_state
        walk_length = random.randrange(2, max_length + 1, 2)
        walk = []; j=0
        negative = False
        while j < walk_length:
            transition_label = random.choice(alphabet)
            if graph.has_outgoing_transition_for_label(current_state, transition_label):
                current_state = graph.get_target_state_for_label(current_state, transition_label)
            else:
                negative = True
            walk.append(transition_label)
            j+=1
        if walk not in negative_walks and negative:
            negative_walks.append(walk)
            i += 1
    return negative_walks

if __name__ == "__main__":
    G = Graph()
    G.set_input_alphabet(['a', 'b'])
    G.set_output_alphabet(['0', '1'])
    state0 = State('q0')
    state1 = State('q1')
    G.graph = {state0:{state1:[Transition(state0, state1, 'a / 0')]},
               state1:{state0:[Transition(state1, state0, 'a / 0')],
                       state1:[Transition(state1, state1, 'b / 1')]}}
    G.set_initial_state(state0)
    pos_walks = generate_positive_walks(3, 4, G, ['a / 0', 'b / 1'])
    for w in pos_walks:
        print(w)
    neg_walks = generate_negative_walks(3, 4, G, ['a / 0', 'b / 1'])
    for w in neg_walks:
        print(w)


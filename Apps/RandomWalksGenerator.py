import random
from copy import copy

from Graph import Graph


def generate_random_walks(graph:Graph, max_length, positive_walks_size, negative_walks_size):
    positive_walks = generate_positive_walks(positive_walks_size, max_length, graph)
    negative_walks = generate_prefixed_closed_negative_walks(negative_walks_size, max_length, graph)

    # positive_walks = []
    # for i in range(positive_walks_size):
    #     walk = []
    #     current_state = graph.initial_state
    #     while long_enough():
    #         input = random.choice(graph.input_alphabet)
    #         output = graph.lambdaFunction(current_state, input)
    #         transition = input + '/' + output
    #         walk.append(transition)
    #         current_state = graph.sigmaFunction(current_state, input)
    #     positive_walks.append(walk)

    return positive_walks

def generate_positive_walks(positive_walks_size, max_length, graph):
    positive_walks = []
    i = 0
    while i < positive_walks_size:
        walk_length = random.randint(1, max_length)
        walk = []
        current_state = graph.initial_state
        for j in range(walk_length):
            input = random.choice(graph.input_alphabet)
            output = graph.get_output(current_state, input)
            transition = input + '/' + output
            walk.append(transition)
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
            output = graph.get_output(current_state, input, graph)
            transition = input + '/' + output
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

if __name__ == '__main__':
    pass
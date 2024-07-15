import random

from Graph import Graph


def generate_random_walks(graph:Graph, max_length, positive_walks_size):
    positive_walks = []
    i=0
    while i <positive_walks_size:
        walk_length = random.randint(1, max_length)
        walk=[]
        current_state = graph.initial_state
        for j in range(walk_length):
            input = random.choice(graph.input_alphabet)
            output = graph.lambdaFunction(current_state, input)
            transition = input+'/'+output
            walk.append(transition)
            current_state = graph.sigmaFunction(current_state, input)
        if walk not in positive_walks:
            positive_walks.append(walk)
            i+=1

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


def long_enough():
    random_float = random.uniform(0, 1)
    return random_float == 0.7





if __name__ == '__main__':

   pass
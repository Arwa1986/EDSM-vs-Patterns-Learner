from Graph import Graph
from State import State
from RandomWalksGenerator import generate_random_walks


def test_get_target_state():
    g = Graph()
    state0 = State('S0', 'accepted', True)
    state1 = State('S1', 'accepted', False)
    state2 = State('S2', 'accepted', False)
    input_alphabet = ['a', 'b']
    output_alphbet = ['1', '2']
    g.graph = {
        state0: {state1: ['a/1'], state0: ['b/1']},
        state1: {state0: ['b/2'], state2: ['a/2']},
        state2: {state1: ['a/1'], state0: ['b/2']},
             }
    g.set_initial_state(state0)
    g.set_input_alphabet(input_alphabet)
    g.set_output_alphabet(output_alphbet)
    g.print_graph()

    positive_examples = generate_random_walks(g, 5, 10)
    print(f'positive example: {positive_examples}')
    print(f'positive examples size: {len(positive_examples)}')

if __name__=="__main__":
    test_get_target_state()
from Graph import Graph
from State import State


def test_set_initail_state_with_exiting_one():
    g = Graph()

    state0 = State('S0', 'accepted', True)
    state1 = State('S1', 'accepted', False)


    g.graph = {state0: {state1:['TansitionA'], state0:['TansitionB']}
             }
    g.graph[state1] = {state0:['TransitionC']}
    g.set_inital_state(state1)
    g.print_graph()

def test_set_initail_state_with_the_same_exiting_one():
    g = Graph()

    state0 = State('S0', 'accepted', True)
    state1 = State('S1', 'accepted', False)


    g.graph = {state0: {state1:['TansitionA'], state0:['TansitionB']}
             }
    g.graph[state1] = {state0:['TransitionC']}
    g.set_inital_state(state0)
    g.print_graph()

if __name__ == "__main__":
    test_set_initail_state_with_exiting_one()
    test_set_initail_state_with_the_same_exiting_one()
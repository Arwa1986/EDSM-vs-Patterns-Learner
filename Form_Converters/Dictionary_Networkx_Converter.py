import networkx as nx
# import matplotlib.pyplot as plt

from Graph import Graph
from State import State
from Transition import Transition


def dictionary_to_networkx(graph_dict):
    # Create an empty MultiDiGraph
    G = nx.MultiDiGraph()

    # Add nodes and edges to the graph
    for src, targets in graph_dict.items():
        for tgt, transitions in targets.items():
            for transition in transitions:
                G.add_edge(src, tgt, transition=transition)

    return G


def dictionary_to_networkx2(graph_dict):
    # Create an empty MultiDiGraph
    G = nx.MultiDiGraph()

    # Add nodes and edges to the graph
    for src, targets in graph_dict.items():
        for tgt, transitions in targets.items():
            for transition in transitions:
                G.add_edge(src.label, tgt.label, label=transition.label)

    return G

def networkx_to_dictionary(graph_networkx:nx.MultiDiGraph):
    # Create an empty graph dictionary
    G = Graph()

    G.set_initial_state(find_initial_state(graph_networkx))

    all_states = graph_networkx.nodes()
    for state in all_states:
        s = State(state)
        G.add_state(s)

    all_edges = graph_networkx.out_edges(data=True)
    for edge in all_edges:
        if edge[2] == {}:
            continue
        G.add_transition(State(edge[0]), State(edge[1]), edge[2]['label'])
    # G.print_graph()
    return G


def find_initial_state(graph):
    for node in graph.nodes:
        if node == 0 or node == 's0' or node == 'S0':
            return State(node)
    return None



if __name__ == "__main__":
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    state3 = State(3)
    state4 = State(4)
    state5 = State(5)
    state6 = State(6)

    transition1 = Transition(state0, state1, 'a/1')
    transition2 = Transition(state1, state2, 'a/2')
    transition3 = Transition(state2, state3, 'b/1')
    transition4 = Transition(state3, state4, 'b/1')
    transition5 = Transition(state1, state5, 'a/1')
    transition6 = Transition(state5, state6, 'b/1')

    graph_dictionary = {
        state0: {state1: [transition1]},
        state1: {state2: [transition2], state5: [transition5]},
        state2: {state3: [transition3]},
        state3: {state4: [transition4]},
        state4: {},
        state5: {state6: [transition6]},
        state6: {}
    }

    graph_networks = dictionary_to_networkx(graph_dictionary)
    # draw_multiDigraph(graph_networks)
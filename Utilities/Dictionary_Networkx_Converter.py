import networkx as nx
import matplotlib.pyplot as plt
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

def draw_multiDigraph(graph):
    # Extract edge labels for visualization
    edge_labels = {(u, v): data['transition'].label for u, v, data in graph.edges(data=True)}

    # Position nodes using pygraphviz layout
    pos = nx.nx_agraph.graphviz_layout(graph, prog='dot')

    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_size=2000)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.title("Graph Visualization with Edge Labels")
    plt.savefig("graph_with_labels.png")
    plt.show()


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
    draw_multiDigraph(graph_networks)
import networkx as nx
import matplotlib.pyplot as plt

def draw_multiDigraph(multiDiGraph, saving_file_path):
    # Extract edge labels for visualization
    edge_labels = {(u, v): data['transition'].label for u, v, data in multiDiGraph.edges(data=True)}

    # Position nodes using pygraphviz layout
    pos = nx.nx_agraph.graphviz_layout(multiDiGraph, prog='dot')

    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(multiDiGraph, pos, with_labels=True, node_size=2000)
    nx.draw_networkx_edge_labels(multiDiGraph, pos, edge_labels=edge_labels)
    plt.title("Graph Visualization with Edge Labels")
    plt.savefig(f"{saving_file_path}.png")
    plt.show()
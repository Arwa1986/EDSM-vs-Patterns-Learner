import networkx as nx
import matplotlib.pyplot as plt

def draw_multiDigraph(multiDiGraph, saving_file_path):
    # Extract edge labels for visualization
    edge_labels = {(u, v): data['label'].label for u, v, data in multiDiGraph.edges(data=True)}

    # Position nodes using pygraphviz layout
    pos = nx.nx_agraph.graphviz_layout(multiDiGraph, prog='dot')

    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(multiDiGraph, pos, with_labels=True, node_size=2000)
    nx.draw_networkx_edge_labels(multiDiGraph, pos, edge_labels=edge_labels)
    plt.title("Graph Visualization with Edge Labels")
    plt.savefig(f"{saving_file_path}.png")
    plt.show()

def draw_multidigraph_with_labels(nx_graph, saving_file_path):
    pos = nx.spring_layout(nx_graph)  # You can also use other layouts like 'dot', 'circular', etc.

    # Draw the nodes with labels
    nx.draw_networkx_nodes(nx_graph, pos, node_size=700)
    nx.draw_networkx_labels(nx_graph, pos, font_size=12, font_family="sans-serif")

    # Draw the edges
    nx.draw_networkx_edges(nx_graph, pos, arrowstyle="->", arrowsize=20)

    # Draw the edge labels manually for MultiDiGraph
    edge_labels = nx.get_edge_attributes(nx_graph, 'label')
    for (u, v, key), label in edge_labels.items():
        # Position label at the midpoint between u and v, with a small offset
        x = (pos[u][0] + pos[v][0]) / 2
        y = (pos[u][1] + pos[v][1]) / 2
        plt.text(x, y, label, fontsize=5, ha='center', va='center', bbox=dict(facecolor='none', edgecolor='none', pad=0.2))

    plt.savefig(f"{saving_file_path}.png")
    plt.show()
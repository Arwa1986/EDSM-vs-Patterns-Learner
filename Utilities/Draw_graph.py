import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc


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

# def draw_multidigraph_with_labels(nx_graph, saving_file_path):
#     pos = nx.spring_layout(nx_graph)  # You can also use other layouts like 'dot', 'circular', etc.
#
#     # Draw the nodes with labels
#     nx.draw_networkx_nodes(nx_graph, pos, node_size=700)
#     nx.draw_networkx_labels(nx_graph, pos, font_size=12, font_family="sans-serif")
#
#     # Draw the edges
#     nx.draw_networkx_edges(nx_graph, pos, arrowstyle="->", arrowsize=20)
#
#     # Draw the edge labels manually for MultiDiGraph
#     edge_labels = nx.get_edge_attributes(nx_graph, 'label')
#     for (u, v, key), label in edge_labels.items():
#         # Position label at the midpoint between u and v, with a small offset
#         x = (pos[u][0] + pos[v][0]) / 2
#         y = (pos[u][1] + pos[v][1]) / 2
#         plt.text(x, y, label, fontsize=5, ha='center', va='center', bbox=dict(facecolor='none', edgecolor='none', pad=0.2))
#
#     plt.savefig(f"{saving_file_path}.png")
#     plt.show()

#
# import matplotlib.pyplot as plt
# import networkx as nx
# import numpy as np

def draw_multidigraph_with_labels(nx_graph, saving_file_path, initial_node_label=None):
    # Use Graphviz layout if available
    try:
        pos = nx.nx_pydot.graphviz_layout(nx_graph, prog='dot')
    except:
        pos = nx.spring_layout(nx_graph)

    # Optionally push the initial node up
    if initial_node_label and initial_node_label in pos:
        pos[initial_node_label] = (pos[initial_node_label][0], pos[initial_node_label][1] + 0.5)

    plt.figure(figsize=(12, 8))

    # Draw nodes
    nx.draw_networkx_nodes(nx_graph, pos, node_size=1000, node_color='lightblue', edgecolors='black', linewidths=1.5)
    nx.draw_networkx_labels(nx_graph, pos, font_size=14, font_weight='bold')

    # Draw edges with slight curvature to avoid overlap
    seen_edges = {}
    for u, v, key in nx_graph.edges(keys=True):
        if (u, v) not in seen_edges:
            seen_edges[(u, v)] = 0
        else:
            seen_edges[(u, v)] += 1

        rad = 0.1 * seen_edges[(u, v)]  # curvature per duplicate edge
        if u == v:
            rad = 0.3 + 0.2 * seen_edges[(u, v)]  # larger radius for self-loops

        nx.draw_networkx_edges(nx_graph, pos, edgelist=[(u, v)], connectionstyle=f'arc3,rad={rad}',
                               arrowstyle='->', arrowsize=25)

    # Draw edge labels, offsetting self-loops and multi-edges
    edge_labels = nx.get_edge_attributes(nx_graph, 'label')
    loop_counters = {}

    for u, v, key in nx_graph.edges(keys=True):
        if u == v:
            # Draw self-loop manually as an arc
            x, y = pos[u]
            loop_radius = 0.2 + 0.1 * key
            arc = Arc((x, y + 0.05), width=0.4, height=0.3, angle=0,
                      theta1=0, theta2=270, color='black')
            plt.gca().add_patch(arc)

            # Draw arrowhead manually
            plt.annotate("",
                         xy=(x, y + 0.2), xytext=(x, y + 0.05),
                         arrowprops=dict(arrowstyle="->", color="black"))

            # Label
            label = nx_graph[u][v][key].get('label', '')
            plt.text(x + 0.3, y + 0.3, label, fontsize=12,
                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
        else:
            # Regular edges
            nx.draw_networkx_edges(nx_graph, pos, edgelist=[(u, v)],
                                   connectionstyle='arc3,rad=0.1',
                                   arrowstyle='->', arrowsize=25)

        # plt.text(x, y, label, fontsize=12, ha='center', va='center',
        #          bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f"{saving_file_path}.png", dpi=300)
    plt.show()

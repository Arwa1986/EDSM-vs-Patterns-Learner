import networkx as nx
import pygraphviz as pgv
import pydot


def dot_to_multidigraph(dot_path):
    # Read the DOT file using pygraphviz
    # The DOT file is opened and read within a with statement,
    # which ensures that the file is closed automatically after its contents are read.
    with open(dot_path, 'r') as f:
        dot_content = f.read()

    agraph = pgv.AGraph(string=dot_content)

    # Convert to a NetworkX MultiDiGraph
    nx_graph = nx.drawing.nx_agraph.from_agraph(agraph)

    # Ensure it is a MultiDiGraph
    if not isinstance(nx_graph, nx.MultiDiGraph):
        nx_graph = nx.MultiDiGraph(nx_graph)

    return nx_graph


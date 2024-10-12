import pydot
from State import State
from Transition import Transition
from Graph import Graph

def dot_to_Graph(dot_file_path):
    # Parse the DOT file
    graphs = pydot.graph_from_dot_file(dot_file_path)
    graph = graphs[0]

    # Create a dictionary to hold the states and transitions
    graph_dictionary = {}

    # Initialize the Graph object
    graph_obj = Graph()

    # Initialize sets for input and output alphabets
    input_alphabet = set()
    output_alphabet = set()

    # Create State objects for each node
    for node in graph.get_nodes():
        state = State(node.get_name())
        graph_dictionary[state] = {}

    # Create Transition objects for each edge and extract input/output
    for edge in graph.get_edges():
        from_state = State(edge.get_source())
        to_state = State(edge.get_destination())
        label = edge.get_label().strip('"')
        input_symbol, output_symbol = label.split(' / ')
        input_alphabet.add(input_symbol)
        output_alphabet.add(output_symbol)
        transition = Transition(from_state, to_state, label)

        if from_state not in graph_dictionary:
            graph_dictionary[from_state] = {}
        if to_state not in graph_dictionary[from_state]:
            graph_dictionary[from_state][to_state] = []
        graph_dictionary[from_state][to_state].append(transition)

    # Set the graph dictionary in the Graph object
    graph_obj.graph = graph_dictionary
    # Set the input and output alphabets in the Graph object
    graph_obj.set_input_alphabet(list(input_alphabet))
    graph_obj.set_output_alphabet(list(output_alphabet))

    # Set the initial state (assuming the first node is the initial state)
    initial_state_label = list(graph.get_nodes())[0].get_name()
    for state in graph_dictionary.keys():
        if state.label == initial_state_label:
            initial_state = state
            graph_obj.set_initial_state(initial_state)
            break



    return graph_obj

# Example usage
# dot_file_path = 'Test/Patterns/extract_patteens_from_reference_DFA/coffeemachine.dot'
# graph_dictionary, graph_obj = dot_to_dictionary(dot_file_path)
# print(graph_dictionary)
# print("Input Alphabet:", graph_obj.input_alphabet)
# print("Output Alphabet:", graph_obj.output_alphabet)
# print("Initial State:", graph_obj.initial_state)
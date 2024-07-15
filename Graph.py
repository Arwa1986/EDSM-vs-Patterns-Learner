from State import State
from Transition import Transition


class Graph:
    def __init__(self):
        self.graph = {}

    def is_empty(self):
        if len(self.graph) == 0:
            return True
        else:
            return False

    def set_initial_state(self, new_state:State):
        self.initial_state = ""
        has_initial = False
        for state, transitions in self.graph.items():
            if state.isInitial:
                has_initial = True
                self.initial_state = state
                if self.initial_state == new_state:
                    return
                print(f"The graph already has an initial state: {self.initial_state}")
                return
        if not has_initial:
            self.initial_state = new_state
            self.initial_state.isInitial = True

    def set_input_alphabet(self, input_alphabet):
        self.input_alphabet = input_alphabet

    def set_output_alphabet(self, output_alphabet):
        self.output_alphabet = output_alphabet

    def add_state(self, state:State):
        if state not in self.graph:
            self.graph[state] = {}

    def get_outgoing_transitions(self, state:State):
        if state in self.graph:
            return self.graph[state]
        else:
            return {}

    # Function to get incoming transitions for a given state
    def get_incoming_transitions(self, target_state):
        incoming_transitions = []
        for state, transitions in self.graph.items():
            for neighbor, transaction_list in transitions.items():
                if neighbor == target_state:
                    for transaction in transaction_list:
                        incoming_transitions.append((state, transaction))
        return incoming_transitions

    def add_transaction(self, from_state:State, to_state:State, transitionLabel):
        if from_state not in self.graph:
            self.addState(from_state)
        if to_state not in self.graph[from_state]:
            self.graph[from_state][to_state]=[]

        new_edge = Transition(from_state, to_state, transitionLabel)
        self.graph[from_state][to_state].append(new_edge)

    def delete_Transition(self, transition:Transition):
        self.graph[transition.from_state][transition.to_state].remove(transition)

    def get_transitions_between_states(self, source, target):
        return self.graph[source][target]

    # lambdaFunction returns the output for a given state with a given input
    # current_state is an State object, input is string
    def get_output(self, current_state, input):
        output = ""
        for to_state, transitions in self.graph[current_state].items():
            for tran in transitions:
                if tran.input == input:
                    return tran.output

        return output

    # returns the target_state for a given state with a given input
    def get_target_state(self, current_state, input):
        target_state = None
        for to_state, transitions in self.graph[current_state].items():
            for tran in transitions:
                if tran.input == input:
                    target_state = to_state

        return target_state

    def has_outgoing_transition_for_label(self, state, transition_label):
        found = False
        for states, transitions in self.graph[state].items():
            for tran in transitions:
                if tran.label == transition_label:
                    found =True
        return found

    # returns the target_state for a given state with a given input
    def get_target_state_for_label(self, current_state, trnsitionLabel):
        target_state = None
        for to_state, transitions in self.graph[current_state].items():
            for tran in transitions:
                if tran.label == trnsitionLabel:
                    target_state = to_state

        return target_state

    # Function to print the graph
    def print_graph(self):
        for state, transitions in self.graph.items():
            print(f"{state}:")
            if transitions:
                for neighbor, transaction in transitions.items():
                    print(f"  -> {neighbor} via {transaction}")
            else:
                print("  No outgoing transitions")

            if state.isInitial:
                print("initial state")
from State import State


class Graph:
    def __init__(self):
        self.graph = {}

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

    def add_transaction(self, from_state, to_state, transitionLabel):
        if from_state not in self.graph:
            self.addState(from_state)
        if to_state not in self.graph[from_state]:
            self.graph[from_state][to_state]=[]

        self.graph[from_state][to_state].append(transitionLabel)

    # lambdaFunction returns the output for a given state with a given input
    def lambdaFunction(self, current_state, input):
        input= input+'/'
        output = ""
        for to_state, transitions in self.graph[current_state].items():
            for tran in transitions:
                if tran.startswith(input):
                    index = tran.find('/')
                    if index != -1:
                        output = tran[index + 1:]

        return output

    # sigmaFunction returns the target_state for a given state with a given input
    def sigmaFunction(self, current_state, input):
        input = input + '/'
        target_state = None
        for to_state, transitions in self.graph[current_state].items():
            for tran in transitions:
                if tran.startswith(input):
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
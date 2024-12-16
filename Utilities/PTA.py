from Graph import Graph
from State import State


class PTA:
    figure_num = 1

    def __init__(self):
        self.G = Graph()
        self.current_state_id = 0

    def add_trace(self, trace):
        input_alphabet_set = set()
        output_alphabet_set = set()
        # if the graph is empty add the first trace
        if self.G.is_empty() :
            current_state = State(self.current_state_id)
            self.G.add_state(current_state)
            self.G.set_initial_state(current_state)

            for i in range(len(trace)):
                #  add transaction
                self.current_state_id += 1
                to_state = State(self.current_state_id)
                self.G.add_state(to_state)
                new_transition = self.G.add_transition(current_state, to_state, trace[i])
                input_alphabet_set.add(new_transition.input)
                output_alphabet_set.add(new_transition.output)
                # the distination now become the source for the next transaction
                current_state = to_state
        else:
            current_state = self.G.initial_state
            current_index = 0
            i=0
            while i  < len(trace):
                if self.G.has_outgoing_transition_for_label(current_state, trace[i]):
                    current_state = self.G.get_target_state_for_label(current_state, trace[i])
                else:
                    current_index = i
                    break
                i+=1
            if current_index < len(trace) and i<len(trace):
                for j in range(current_index, len(trace)):
                    #  add transaction
                    self.current_state_id += 1
                    to_state = State(self.current_state_id)
                    self.G.add_state(to_state)
                    new_transition = self.G.add_transition(current_state, to_state, trace[j])
                    input_alphabet_set.add(new_transition.input)
                    output_alphabet_set.add(new_transition.output)
                    # the distination now become the source for the next transaction
                    current_state = to_state
        # add a special self-loop transition at the end of each trace.
        # this transition is used for the porspose of NuSMS model checker.
        # NuSMV generates a counterexample if there is an infinite sequence of events.
        new_transition = self.G.add_transition(current_state, current_state, 'to_be_continued / add_transition')
        input_alphabet_set.add(new_transition.input)
        output_alphabet_set.add(new_transition.output)
        return input_alphabet_set, output_alphabet_set

    def build_pta(self, positive_traces):
        all_input = set()
        all_output = set()
        for t in positive_traces:
            input_set, output_set = self.add_trace(t)
            for i in input_set:
                all_input.add(i)
            for o in output_set:
                all_output.add(o)
        return list(all_input), list(all_output)

    def add_trace_for_labeled_pta(self,RefDFA_G, trace):
        input_alphabet_set = set()
        output_alphabet_set = set()
        currentStateRefDFA = RefDFA_G.initial_state
        # if the graph is empty add the first trace
        if self.G.is_empty() :
            current_state = State(self.current_state_id)
            current_state.set_reference_state(currentStateRefDFA)
            self.G.add_state(current_state)
            self.G.set_initial_state(current_state)

            for i in range(len(trace)):
                # add new state to the PTA + label it with the next state of the reference DFA
                RefDFA_to_state = RefDFA_G.get_target_state_for_label(currentStateRefDFA, trace[i])
                self.current_state_id += 1
                to_state = State(self.current_state_id)
                to_state.set_reference_state(RefDFA_to_state)
                self.G.add_state(to_state)
                #  add transaction
                new_transition = self.G.add_transition(current_state, to_state, trace[i])
                input_alphabet_set.add(new_transition.input)
                output_alphabet_set.add(new_transition.output)
                # the distination now become the source for the next transaction
                current_state = to_state
                currentStateRefDFA = RefDFA_to_state
        else:
            current_state = self.G.initial_state
            current_index = 0
            i=0
            while i  < len(trace):
                if self.G.has_outgoing_transition_for_label(current_state, trace[i]):
                    current_state = self.G.get_target_state_for_label(current_state, trace[i])
                    currentStateRefDFA = RefDFA_G.get_target_state_for_label(currentStateRefDFA, trace[i])
                else:
                    current_index = i
                    break
                i+=1
            if current_index < len(trace) and i<len(trace):
                for j in range(current_index, len(trace)):
                    # add new state to the PTA + label it with the next state of the reference DFA
                    RefDFA_to_state = RefDFA_G.get_target_state_for_label(currentStateRefDFA, trace[j])
                    self.current_state_id += 1
                    to_state = State(self.current_state_id)
                    to_state.set_reference_state(RefDFA_to_state)
                    self.G.add_state(to_state)
                    #  add transaction
                    new_transition = self.G.add_transition(current_state, to_state, trace[j])
                    input_alphabet_set.add(new_transition.input)
                    output_alphabet_set.add(new_transition.output)
                    # the distination now become the source for the next transaction
                    current_state = to_state
                    currentStateRefDFA = RefDFA_to_state
        # add a special self-loop transition at the end of each trace.
        # this transition is used for the porspose of NuSMS model checker.
        # NuSMV generates a counterexample if there is an infinite sequence of events.
        new_transition = self.G.add_transition(current_state, current_state, 'to_be_continued / add_transition')
        input_alphabet_set.add(new_transition.input)
        output_alphabet_set.add(new_transition.output)
        return input_alphabet_set, output_alphabet_set

    def build_labeled_pta(self,RefDFA, positive_traces):
        all_input = set()
        all_output = set()
        for t in positive_traces:
            input_set, output_set = self.add_trace_for_labeled_pta(RefDFA, t)
            for i in input_set:
                all_input.add(i)
            for o in output_set:
                all_output.add(o)
        return list(all_input), list(all_output)

if __name__ == "__main__":
    pta = PTA()
    pta.add_trace(['a/1', 'a/2', 'b/1', 'b/1'])
    pta.add_trace(['a/1', 'a/1', 'b/1'])
    pta.G.print_graph()
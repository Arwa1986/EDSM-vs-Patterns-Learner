from Graph import Graph
from State import State


class PTA:
    figure_num = 1

    def __init__(self):
        self.G = Graph()
        self.current_state_id = 0

    def add_trace(self, trace):
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
                self.G.add_transaction(current_state, to_state, trace[i])
                # the distination now become the source for the next transaction
                current_state = to_state
        else:
            current_state = self.G.initial_state
            current_index = 0
            for i in range(len(trace)):
                if self.G.has_outgoing_transition_for_label(current_state, trace[i]):
                    current_state = self.G.get_target_state_for_label(current_state, trace[i])
                else:
                    current_index = i
                    break
            if current_index != (len(trace)-1):
                for j in range(current_index, len(trace)):
                    #  add transaction
                    self.current_state_id += 1
                    to_state = State(self.current_state_id)
                    self.G.add_state(to_state)
                    self.G.add_transaction(current_state, to_state, trace[j])
                    # the distination now become the source for the next transaction
                    current_state = to_state

    def build_pta(self, positive_traces):
        for t in positive_traces:
            self.add_trace(t)

if __name__ == "__main__":
    pta = PTA()
    pta.add_trace(['a/1', 'a/2', 'b/1', 'b/1'])
    pta.add_trace(['a/1', 'a/1', 'b/1'])
    pta.G.print_graph()
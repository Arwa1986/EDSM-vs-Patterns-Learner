from Patterns.Pattern import Pattern
from Utilities.Pattern import get_actual_output_for_input_sequence


class Output_for_input_sequence_pattern(Pattern):
    def __init__(self, input_sequence, output):
        super().__init__('output_for_input_sequence_pattern')
        self.input_sequence = input_sequence
        self.output = output

    def print(self):
        print(f'{self.input_sequence}-->{self.output}')

    def __lt__(self, other):
        return (self.input_sequence, self.output) < (other.input_sequence, other.output)
    def __eq__(self, other):
        return (self.input_sequence == other.input_sequence) and (self.output == other.output)
    def violated_by_partial_graph(self, partial_graph): #parial_graph:Learner
        violate = False

        actual_output = get_actual_output_for_input_sequence(self.input_sequence, partial_graph.pta.G, partial_graph.red_states)
        if actual_output != self.output:
            print(f' the last merge violates pattern: Expected_output_for_input_sequence')
            print(f'This sequence of input should have {self.output} as the only output')
            violate = True

        return violate


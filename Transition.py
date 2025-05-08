import re


class Transition:
    def __init__(self, from_state, to_state, label):
        self.from_state = from_state
        self.to_state = to_state
        self.label = label
        self.input = ''
        self.output = ''
        self.set_input_output()


    def __repr__(self):
        return f'Transition({self.label})'

    def __eq__(self, other):
        if isinstance(other, Transition):
            return self.label == other.label and self.from_state == other.from_state and self.to_state == other.to_state
        return False
    def __hash__(self):
        return hash((self.from_state, self.to_state, self.label))

    def set_input_output(self):
        # index = self.label.find(' / ')
        # if index != -1:
        #     self.input = self.label[:index]
        #     self.output = self.label[index + 3:]
        # input output are sperated by / with or without white space
        match = re.search(r'\s*/\s*', self.label)
        if match:
            input_end = match.start()
            output_start = match.end()
            self.input = self.label[:input_end]
            self.output = self.label[output_start:]

    def is_self_loop(self):
        return self.from_state == self.to_state
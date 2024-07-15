class Transition:
    def __init__(self, from_state, to_state, label):
        self.from_state = from_state
        self.to_state = to_state
        self.label = label
        self.set_input_output()


    def __repr__(self):
        return f'Transition({self.label})'

    def set_input_output(self):
        index = self.label.find('/')
        if index != -1:
            self.input = self.label[:index]
            self.output = self.label[index + 1:]
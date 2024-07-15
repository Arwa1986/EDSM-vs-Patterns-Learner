class Transition:
    def __init__(self, _from, to, input, output):
        self._from = _from
        self.to = to
        self.input = input
        self.output = output
        self.label = str(input)+"/"+str(output)

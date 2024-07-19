class State:

    def __init__(self, label, type="unlabeled", isInitial=False):
            self.label = label
            self.type = type
            self.isInitial = isInitial
            self.color = "white"

    def __hash__(self):
        return hash(self.label)

    def __repr__(self):
        return f'State({self.label})'

    def __eq__(self, other):
        if isinstance(other, State):
            return self.label == other.label
        return False

    def getIncomingTransitions(self):
        pass

    def getOutgoingTransitions(self):
        pass

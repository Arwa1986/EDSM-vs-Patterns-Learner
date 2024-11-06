from State import State
from Transition import Transition

dictionary = {State(0): {
        State(1): [Transition(State(0), State(1), "open / 1")],
        State(4): [Transition(State(0), State(4), "load / 1")]
    },
    State(1): {
        State(2): [Transition(State(1), State(2), "edit / 1")]
    }
}

for state, transitions in dictionary.items():
    if state.label in [0,4,6,9] and state.color=='white':
        print (state.label)
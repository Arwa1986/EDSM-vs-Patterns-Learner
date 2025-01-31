from EventsInPairs.random_traces_generator import generate_positive_walks, generate_negative_walks
from EventsInPairs.traces_in_scarlet_format import to_scarlet_format
from Graph import Graph
from State import State
from Transition import Transition
from Utilities.write_clear_file import write_to_file_in_new_line, clear_file, write_to_file_in_line
from Scarlet.ltllearner import LTLlearner
if __name__ == "__main__":
    G = Graph()
    G.set_input_alphabet(['a', 'b'])
    G.set_output_alphabet(['0', '1'])
    state0 = State('q0')
    state1 = State('q1')
    G.graph = {state0: {state1: [Transition(state0, state1, 'a / 0')]},
               state1: {state0: [Transition(state1, state0, 'a / 0')],
                        state1: [Transition(state1, state1, 'b / 1')]}}
    G.set_initial_state(state0)
    pos_walks = generate_positive_walks(3, 4, G, ['a / 0', 'b / 1'])
    print("Positive walks")
    for w in pos_walks:
        print(w)

    alphabet = ['a / 0 , a / 0', 'a / 0 , b / 1', 'b / 1 , a / 0', 'b / 1 , b / 1']
    clear_file('scarlet_input.txt')

    print("Positive walks in scarlet format")
    for pw in pos_walks:
        pw_sarlet_format = to_scarlet_format(pw,alphabet)
        print(pw_sarlet_format)

        write_to_file_in_new_line('scarlet_input.txt', pw_sarlet_format)
    write_to_file_in_new_line('scarlet_input.txt', '---')
    neg_walks = generate_negative_walks(3, 4, G, ['a / 0', 'b / 1'])
    print("Negative walks")
    for w in neg_walks:
        print(w)

    print("Negative walks in scarlet format")
    for nw in neg_walks:
        nw_scarlet_format = to_scarlet_format(nw, alphabet)
        print(nw_scarlet_format)
        write_to_file_in_new_line('scarlet_input.txt', nw_scarlet_format)
    write_to_file_in_new_line('scarlet_input.txt', '---\n---')

    alphabet = ['a/0 _ a/0', 'a/0 _ b/1', 'b/1 _ a/0', 'b/1 _ b/1']
    for a in alphabet:
        # alphabet_str += a
        if alphabet.index(a) == len(alphabet) - 1:
            write_to_file_in_line('scarlet_input.txt', a)
            break
        write_to_file_in_line('scarlet_input.txt', a+',')

    # 2- run Scarlet
    input_file_path = "scarlet_input.txt"
    learner = LTLlearner(input_file=input_file_path, csvname="result.csv")
    learner.learn()
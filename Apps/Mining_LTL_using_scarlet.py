from RandomWalksGenerator import generate_random_walks
from Form_Converters.GraphObj_DotFile_converter import dot_to_Graph
from Traces.reform_traces_into_scarlet_form import to_scarlet_form
from Scarlet.ltllearner import LTLlearner

from Utilities.write_clear_file import clear_file, write_to_file_in_new_line, write_to_file_in_line

if __name__ == '__main__':
    # 1- Generate Random Walks
    # 1-1 dot to Dictionary
    # CM_Graph = dot_to_Graph('../TextEditorSystem/TextEditor_no_sink_state.dot')

    # 1-2 generate random walks
    # positive_walks, negative_walks = generate_random_walks(CM_Graph, 5, 8, 10)

    alphabet = ['load/1', 'open/1', 'edit/1', 'save/1', 'exit/2']
    positive_walks = [
        ['load/1', 'open/1', 'edit/1', 'save/1', 'exit/2'],
        ['load/1', 'open/1', 'edit/1', 'edit/1', 'edit/1', 'edit/1', 'save/1'],
        ['open/1', 'edit/1', 'edit/1'],
        ['load/1', 'open/1', 'exit/2'],
        ['open/1', 'edit/1', 'save/1', 'exit/2'],
        ['open/1', 'edit/1', 'save/1', 'exit/2', 'load/1', 'open/1', 'edit/1', 'save/1', 'exit/2']
    ]
    clear_file('scarlet_input.txt')
    for pw in positive_walks:
        walk_in_sacarlet_form = to_scarlet_form(pw, alphabet)
        write_to_file_in_new_line('scarlet_input.txt', walk_in_sacarlet_form)

    write_to_file_in_new_line('scarlet_input.txt', '---\n---\n---')
    # alphabet_str = ''
    for a in alphabet:
        # alphabet_str += a
        if alphabet.index(a) == len(alphabet) - 1:
            write_to_file_in_line('scarlet_input.txt', a)
            break
        write_to_file_in_line('scarlet_input.txt', a+',')

    # write_to_file_in_new_line('scarlet_input.txt', alphabet_str)

    # 2- run Scarlet
    input_file_path = "scarlet_input.txt"
    learner = LTLlearner(input_file=input_file_path, csvname="result.csv")
    learner.learn()

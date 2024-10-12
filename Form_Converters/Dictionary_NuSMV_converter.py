
def dictionary_to_NuSMV(graph_obj):
    graph_size = len(graph_obj.get_all_states())
    contents = 'MODULE main\nVAR\nstate:{'

    states = graph_obj.get_all_states()
    for s in range(len(states)):
        contents += f'{states[s]}'
        if s < len(states)-1:
            contents += ', '
    contents += f'}};\n'

    contents += f'input:{{'
    inputs = graph_obj.get_input_alphabet()
    for i in range(len(inputs)):
        contents += f'{inputs[i]}'
        if i < len(inputs)-1:
            contents += ', '
    contents += f'}};\n'

    contents += f'output:{{'
    outputs = graph_obj.get_output_alphabet()
    for o in range(len(outputs)):
        contents += f'{outputs[o]}'
        if o < len(outputs) - 1:
            contents += ', '
    contents += f'}};\n'

    contents += f'ASSIGN\ninit(state):={graph_obj.initial_state};\nnext(state):=case\n'
    for t in graph_obj.get_all_transitons():
        contents += f'state = {t.from_state} & input = {t.input} : {t.to_state};\n'
    contents += f'esac;\n'

    contents += f'next(output):=case\n'
    for t in graph_obj.get_all_transitons():
        contents += f'state = {t.from_state} & input = {t.input} : {t.output};\n'
    contents += f'esac;\n'

    return contents



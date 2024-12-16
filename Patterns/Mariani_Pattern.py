from Utilities.PTA import PTA
from smv.smv_engin import run_nusmv, parse_nusmv_output


def get_ifXenevntuallyY_patterns(pta):
    # 1- get all existing labels
    labels_set = pta.G.get_transitions_labels_set()
    # remove the labels that are not useful
    if ('to_be_continued', 'add_transition') in labels_set:
        labels_set.remove(('to_be_continued', 'add_transition'))

    # 2- design all possible patterns
    patterns = []
    for x_label in labels_set:
        for y_label in labels_set:
            if x_label != y_label:
                x = f'input={x_label[0]} & output={x_label[1]}'
                y = f'input={y_label[0]} & output={y_label[1]}'
                if_x_enevntually_y = f'G ((! ({x})) | F(({x})) & F ({y})))'
                patterns.append(if_x_enevntually_y)
    return patterns

def get_ifXnoYwithin2steps_patterns(pta):
    # 1- get all existing labels
    labels_set = pta.G.get_transitions_labels_set()
    # remove the labels that are not useful
    if ('to_be_continued', 'add_transition') in labels_set:
        labels_set.remove(('to_be_continued', 'add_transition'))

    # 2- design all possible patterns
    patterns = []
    for x_label in labels_set:
        for y_label in labels_set:
            if x_label != y_label:
                x = f'input={x_label[0]} & output={x_label[1]}'
                y = f'input={y_label[0]} & output={y_label[1]}'
                if_x_no_y_within_2_steps = f'G ((! ({x})) | (({x} -> X !({y})) & X (X!({y})) ))'
                patterns.append(if_x_no_y_within_2_steps)
    return patterns

def get_safety_patterns(pta):
    # patterns = get_ifXenevntuallyY_patterns(pta)
    patterns = get_ifXnoYwithin2steps_patterns(pta)
    # print('===========All-Patterns:=============')
    # for p in patterns:
    #     print(p)
    graph_SMV = pta.G.to_nusmv(patterns)

    output, err = run_nusmv(graph_SMV)
    specs = parse_nusmv_output(output)

    # positive patterns are the one that must never be violated during the merging process
    # positive patterns has 100% confidence, which means that they are always true.
    # in other words, whenever x occur, y must eventually follow.
    positive_patterns = []
    for p in specs:
        if p.success:
            positive_patterns.append(f'{p.condition}')
    return positive_patterns



if __name__ == '__main__':
    traces = [['open / 1', 'edit / 1', 'save / 1', 'exit / 2'],
              ['open / 1', 'edit / 1', 'edit / 1']]

    pta = PTA()  # Create a PTA object
    pta.build_pta(traces)  # Build the PTA with the given traces

    get_ifXenevntuallyY_patterns(pta)  # Generate and print Mariani patterns
def to_scarlet_format(trace, alphabet):
    # in pairs of events
    scarlet_trace= ''
    for i in range(0, len(trace), 2):
        event = trace[i]+ ' , ' + trace[i + 1]
        truth_value = ''
        for a in alphabet:
            if event == a:
                truth_value += '1'
            else:
                truth_value += '0'
            if alphabet.index(a) != len(alphabet) - 1:
                truth_value += ','
        scarlet_trace += truth_value
        if i != len(trace) - 2:
            scarlet_trace += ';'
    return scarlet_trace

if __name__ == "__main__":
    alphabet = ['a , a', 'a , b', 'b , a', 'b , b']
    trace = ['a', 'b', 'a', 'a', 'b', 'b', 'b', 'b']
    s_trace = to_scarlet_format(trace, alphabet)

    for t in s_trace:
        print(t)


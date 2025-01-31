def to_scarlet_form(original_form, alphabet):
    scarlet_trace = []
    for label in original_form:
        index = alphabet.index(label)
        word = ''
        for i in range (len(alphabet)):
            if i == index:
                 word += '1'
            else:
                word+='0'
            if i == len(alphabet)-1:
                continue
            word+= ','
        scarlet_trace.append(word)

    scarlet_trace_str=''
    temp_index = 0
    for word in scarlet_trace:
        scarlet_trace_str+=word
        if temp_index == len(scarlet_trace)-1:
            break
        else:
            scarlet_trace_str += ';'
        temp_index += 1

    return scarlet_trace_str


if __name__ == '__main__':
    original_trace = ['open/1', 'edit/1', 'edit/1', 'edit/1', 'exit/2']
    alphabet=['open/1', 'edit/1', 'exit/2']

    print(to_scarlet_form(original_trace, alphabet))
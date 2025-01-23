
def textbreaker(input):
    textbroke = []
    sentence = []
    string = ''
    for letter in input:
        if letter == ' ':
            if string != '':
                sentence.append(string)
                string = ''
        else:
            string = string+letter     
        if letter == '.' or letter == '?':
            if string[-3:] != 'Mr.' and string[-4:] != 'Mrs.' and string[-3:] != 'Dr.':
                sentence.append(string)
                string = ''
                textbroke.append(sentence)
                sentence = []
    if letter != '.' and letter != '?':
        textbroke.append(string)

    return textbroke
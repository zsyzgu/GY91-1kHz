import sys
import os
import analyze_model
import numpy as np
import utils

output = None

def get_grams(task, id):
    str = task[id]
    str += ' '
    if id - 1 >= 0:
        str += task[id - 1]
    else:
        str += 'None'
    str += ' '
    if id - 2 >= 0:
        str += task[id - 2]
    else:
        str += 'None' 
    return str

def analyze_session(file, session):
    task = []
    inputed = []
    inputed_letters = []
    word_buffer = []
    phrase_buffer = []

    lines = [line.strip() for line in open(file, 'r').readlines()]
    for line in lines:
        tags = line.split()
        command = tags[1]
        if command == 'START_PHRASE':
            inputed = []
            phrase_buffer = []
            inputed_letters = []
            word_buffer = []
            task = tags[2:]
        if command == 'ENTRY_A_LETTER':
            if (len(inputed) < len(task)):
                word = task[len(inputed)]
                if len(inputed_letters) < len(word):
                    letter = word[len(inputed_letters)]
                    inputed_letters.append(letter)
                    word_buffer.append(' '.join(tags[2:]) + ' ' + letter)
        if command == 'ENTRY_A_WORD':
            if len(tags) == 3:
                inputed.append(tags[2])
                inputed_letters = []
                phrase_buffer.append(word_buffer)
                word_buffer = []
            else:
                command = 'DELETE_LETTERS'
        if command == 'DELETE_A_WORD':
            if len(inputed) > 0:
                if len(inputed[-1]) == len(phrase_buffer[-1]):
                    output.write(inputed[-1] + ' ' + str(session) + ' ' + get_grams(task, len(inputed) - 1) + ' N\n')
                    for letter_info in phrase_buffer[-1]:
                        output.write(letter_info + '\n')
                inputed.pop(-1)
                phrase_buffer.pop(-1)
                inputed_letters = []
                word_buffer = []
                if len(inputed) == 0:
                    inputed = []
                    phrase_buffer = []
        if command == 'DELETE_LETTERS':
            inputed_letters = []
            word_buffer = []
        if command == 'END_PHRASE':
            flag = (tags[2] == 'True') and (len(task) == len(inputed))
            if flag:
                for i in range(len(phrase_buffer)):
                    word_buffer = phrase_buffer[i]
                    word = task[i]
                    is_correct = 'Y'
                    if inputed[i] != word:
                        is_correct = 'N'
                    if len(inputed[i]) == len(word):
                        output.write(word + ' ' + str(session) + ' ' + get_grams(task, i) + ' ' + is_correct + '\n')
                        for letter_info in word_buffer:
                            output.write(letter_info + '\n')

if __name__ == "__main__":
    root = './data-main/'
    if (len(sys.argv) != 2):
        print '[User] required.'
        exit()
    user = sys.argv[1]

    output = open('./data-person/' + user + '.txt', 'w')
    for file in os.listdir(root):
        name = file.split('_')[0]
        session = int(file.split('_')[1].split('.')[0])
        if name == user:
            analyze_session(root + '/' + file, session)

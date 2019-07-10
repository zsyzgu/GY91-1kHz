import sys
import os
import analyze_model
import numpy as np

def analyze_session(file):
    output = open('fake_study2_log.txt', 'w')
    last_info = None

    task = []
    is_started = False
    corrected = 0
    inputed = []
    inputed_letters = []
    word_buffer = []
    phrase_buffer = []

    lines = [line.strip() for line in open(file, 'r').readlines()]
    for line in lines:
        tags = line.split()
        if (len(tags) == 13):
            last_info = line
        command = tags[1]
        if command == 'START_PHRASE':
            is_started = False
            corrected = 0
            inputed = []
            phrase_buffer = []
            task = tags[2:]
        if command == 'ENTRY_A_LETTER':
            if is_started == False:
                is_started = True
            if (len(inputed) < len(task)):
                word = task[len(inputed)]
                if len(inputed_letters) < len(word):
                    letter = word[len(inputed_letters)]
                    inputed_letters.append(letter)
                    word_buffer.append(str(last_info) + ' ' + letter)
        if command == 'ENTRY_A_WORD':
            if len(tags) == 3:
                inputed.append(tags[2])
                inputed_letters = []
                phrase_buffer.append(word_buffer)
                word_buffer = []
        if command == 'DELETE_A_WORD':
            if len(inputed) > 0:
                inputed.pop(-1)
                phrase_buffer.pop(-1)
                corrected += 1
                if len(inputed) == 0:
                    is_started = False
                    corrected = 0
                    inputed = []
                    phrase_buffer = []
        if command == 'DELETE_LETTERS':
            if len(inputed) == 0:
                is_started = False
                corrected = 0
                inputed = []
            inputed_letters = []
            word_buffer = []
        if command == 'END_PHRASE':
            for word_buffer in phrase_buffer:
                for letter_info in word_buffer:
                    print letter_info
                    output.write(letter_info + '\n')
            flag = (tags[2] == 'True')
            if flag:
                print last_info, 'Y'
                output.write(last_info + ' Y\n')
            else:
                print last_info, 'N'
                output.write(last_info + ' N\n')

if __name__ == "__main__":
    root = './data-main/'
    
    if (len(sys.argv) != 3):
        print '[User & Session] required.'
        exit()

    user = sys.argv[1]
    session = sys.argv[2]
    if session == '-A':
        session = 100
    else:
        session = int(session)

    for file in os.listdir(root):
        name = file.split('_')[0]
        id = int(file.split('_')[1].split('.')[0])
        if name == user and id < session:
            analyze_session(root + '/' + file)

import sys
import os
import analyze_model
import numpy as np

output = None

def analyze_session(file):
    last_info = None

    task = []
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
                    word_buffer.append(str(last_info) + ' ' + letter)
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
            cnt = 0
            pred = ''
            for word_buffer in phrase_buffer:
                for letter_info in word_buffer:
                    # print letter_info
                    output.write(letter_info + '\n')
                    cnt += 1
                    pred += letter_info[-1]
                pred += ' '
            flag = (tags[2] == 'True') and (' '.join(task) == ' '.join(inputed))
            if flag:
                if pred[:-1] != ' '.join(task):
                    print ' '.join(task)
                    print ' '.join(inputed)
                    print pred
                # print last_info, 'Y'
                output.write(last_info + ' Y\n')
            else:
                # print last_info, 'N'
                output.write(last_info + ' N\n')

if __name__ == "__main__":
    root = './data-main/'
    
    if (len(sys.argv) != 3):
        print '[User & Session] required.'
        exit()

    user = sys.argv[1]
    session = sys.argv[2]

    users = []
    if user == "-A":
        for f in os.listdir(root):
            f = f.split("_")[0]
            if f not in users:
                users.append(f)
    else:
        users.append(user)
    
    for user in users:
        print(user)
        if session == '-A':
            session = 100
        else:
            session = int(session)
        output = open('./data-fake/' + user + '_' + str(session) + '.txt', 'w')

        for file in os.listdir(root):
            name = file.split('_')[0]
            id = int(file.split('_')[1].split('.')[0])
            if name == user and id < session:
                analyze_session(root + '/' + file)

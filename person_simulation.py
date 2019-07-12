import sys
import os
import entry
import analyze_model
import numpy as np

root = './data-person/'

def train(user, session):
    file = root + user + '.txt'
    lines = [line.strip() for line in open(file, 'r')]

    i = 0
    data = []
    while i < len(lines):
        line = lines[i]
        tags = line.split()
        word = tags[0]
        word_session = int(tags[1])
        is_correct = (tags[5] == 'Y')
        is_train_data = is_correct and word_session < session
        length = len(word)
        task_word = tags[2]
        if is_train_data:
            pitchs = []
            headings = []
            for j in range(length):
                tags = lines[i + 1 + j].split()
                pitch = float(tags[0])
                heading = float(tags[1])
                pitchs.append(pitch)
                headings.append(heading)
            last_row = None
            last_col = None
            for j in range(length):
                letter = task_word[j]
                row = entry.Entry.layout[letter][1]
                col = entry.Entry.layout[letter][0]
                if last_row != None:
                    data.append([row, col, last_row, last_col, pitchs[j], headings[j] - headings[j - 1]])
                last_row = row
                last_col = col
        i += length + 1
    data = np.array(data).reshape(-1, 6)
    analyze_model.output_model(data, user)

def simulate_word(text_entry, word, pitchs, headings):
    candidates = text_entry.predict(pitchs, headings)
    id = -1
    for i in range(text_entry.MAX_CANDIDATES):
        if word == candidates[i]:
            id = i
            break
    return id

def test(user, session, is_P_model):
    if is_P_model:
        text_entry = entry.Entry(5000, entry.LanguageModel.USE_TRIGRAMS, user)
    else:
        text_entry = entry.Entry(5000, entry.LanguageModel.USE_TRIGRAMS)
    result = [0] * (text_entry.MAX_CANDIDATES + 1)
    
    file = root + user + '.txt'
    lines = [line.strip() for line in open(file, 'r')]

    i = 0
    while i < len(lines):
        line = lines[i]
        tags = line.split()
        word = tags[0]
        word_session = int(tags[1])
        is_test_data = word_session >= session
        length = len(word)
        task_word = tags[2]
        gram_1 = tags[3]
        gram_2 = tags[4]
        if gram_1 == 'None':
            gram_1 = None
        if gram_2 == 'None':
            gram_2 = None
        if is_test_data:
            pitchs = []
            headings = []
            for j in range(length):
                tags = lines[i + 1 + j].split()
                pitch = float(tags[0])
                heading = float(tags[1])
                pitchs.append(pitch)
                headings.append(heading)
            text_entry.language_model.update_grams(gram_1, gram_2)
            id = simulate_word(text_entry, task_word, pitchs, headings)
            if id == -1:
                result[text_entry.MAX_CANDIDATES] += 1
            else:
                result[id] += 1

        i += length + 1
    
    output = user
    total = sum(result)
    if total > 0:
        for i in range(len(result)):
            result[i] = float(result[i]) / total
            output += ' ' + str(round(result[i] * 100, 2)) + '%'
        print output
    else:
        print 'No test data'

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print '[User and Session] required.'
        exit()
    user = sys.argv[1]
    session = int(sys.argv[2])

    train(user, session)
    
    print '=== P Model ==='
    test(user, session, True)
    print '=== G Model ==='
    test(user, session, False)

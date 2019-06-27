import entry
import utils
import entry
import numpy as np
import time

root = './data-model/'
layout = entry.Entry.layout
phrases = [line.strip() for line in open('phrases.txt', 'r').readlines()]
entry = entry.Entry(3000, entry.LanguageModel.USE_TRIGRAMS)
entry.MAX_CANDIDATES = 5
result = [0] * (entry.MAX_CANDIDATES + 1)

def simulate_word(word, pitchs, headings):
    global result
    if word not in entry.words:
        return
    candidates = entry.predict(pitchs, headings)
    id = -1
    for i in range(entry.MAX_CANDIDATES):
        if word == candidates[i]:
            id = i
            break
    if id == -1:
        result[entry.MAX_CANDIDATES] += 1
    else:
        result[id] += 1

def simulate(task, pitchs, headings):
    length = len(''.join(task))
    if len(pitchs) < length:
        print 'Not completed'
        return
    entry.update_grams(None, None)
    tot = 0
    last_word = None
    for word in task:
        simulate_word(word, pitchs[tot : tot + len(word)], headings[tot : tot + len(word)])
        if entry.language_model.LM >= entry.language_model.USE_BIGRAMS:
            entry.update_grams(word, last_word)
        tot += len(word)
        last_word = word

def analyze_file(file):
    lines = [line.strip() for line in open(file, 'r').readlines()]
    inputed = ''
    pitchs = []
    headings = []

    for line in lines:
        tags = line.split()
        remark = tags[-1]
        pitch = float(tags[10])
        heading = float(tags[11])

        if remark == 'Y':
            task = ''
            for phrase in phrases:
                if str.lower(''.join(phrase.split())) == inputed:
                    task = phrase
            task = task.split()
            simulate(task, pitchs, headings)
            inputed = ''
            pitchs = []
            headings = []
        elif remark == 'N':
            inputed = ''
            pitchs = []
            headings = []
        elif remark != '-' and remark != '#':
            inputed += str.lower(remark)
            pitchs.append(pitch)
            headings.append(heading)

def analyze_user(user):
    global result
    result = [0] * (entry.MAX_CANDIDATES + 1)

    file_names = utils.get_all_file_name(root + user + '_')
    for file_name in file_names:
        analyze_file(file_name)

    output = user
    total = sum(result)
    for i in range(len(result)):
        result[i] = float(result[i]) / total
        output += ' ' + str(round(result[i] * 100, 2)) + '%'
    print output
    return result[0]


start_time = time.time()
total_result = []

users = utils.get_users(root)
for user in users:
    total_result.append(analyze_user(user))

total_result = np.array(total_result)
print np.mean(total_result), np.std(total_result)
print 'Escaped Time =', time.time() - start_time

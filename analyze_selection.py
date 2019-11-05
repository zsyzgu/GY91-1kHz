from analyze_time import analyze_session_with_timestamp
import utils
import os
from person_simulation import train, combine_GP
import entry
import numpy as np
from matplotlib import pyplot as plt

p_user = ["gyz", "syt", "xcy", "ljs", "lw", "cwh", "wjs", "lsm"]
g_user = ["lzp", "xt", "xjj", "zzy", "lry", "lmm", "lq", "zwx"]

select = [[], [], [], [], []]
result = [[], [], [], [], []]

def simulate_word(text_entry, word, pitchs, headings):
    candidates = text_entry.predict(pitchs, headings)
    id = -1
    for i in range(text_entry.MAX_CANDIDATES):
        if word == candidates[i]:
            id = i
            break
    return id

def test_selection(user, session, is_P_model):
    if is_P_model:
        text_entry = entry.Entry(5000, entry.LanguageModel.USE_TRIGRAMS, user)
    else:
        text_entry = entry.Entry(5000, entry.LanguageModel.USE_TRIGRAMS)
    result = [0] * (text_entry.MAX_CANDIDATES + 1)
    
    file = "./data-person/" + user + '.txt'
    lines = [line.strip() for line in open(file, 'r')]

    i = 0
    while i < len(lines):
        line = lines[i]
        tags = line.split()
        word = tags[0]
        word_session = int(tags[1])
        # is_test_data = word_session < session
        is_test_data = (session <= word_session and word_session < session + 3)
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
                pitch = float(tags[1])
                heading = float(tags[2])
                pitchs.append(pitch)
                headings.append(heading)
            last_up = int(lines[i + length].split()[0])
            selection = int(lines[i + length + 1].split()[0])
            text_entry.language_model.update_grams(gram_1, gram_2)
            id = simulate_word(text_entry, task_word, pitchs, headings)
            if id == -1:
                # print((line) )
                result[text_entry.MAX_CANDIDATES] += 1
            else:
                select[id].append(float(selection - last_up) / 1e6)
                result[id] += 1

        i += length + 2
    
    output = user
    total = sum(result)
    if total > 0:
        for i in range(len(result)):
            result[i] = float(result[i]) / total
            output += ' ' + str(round(result[i] * 100, 2)) + '%'
        print( output )
        return output
    else:
        print( 'No test data' )

def draw_selection():
    with open("./select_time.txt", "r") as f:
        lines = f.readlines()
        i = 1
        while i < len(lines):
            if lines[i - 1].strip().split()[0] == "wjs":
                i += 2
                continue
            line = lines[i].strip().split()
            for j in range(5):
                result[j].append(float(line[j]))
            i += 2
    result_mean = []
    result_std = []
    for i in range(5):
        result_mean.append(np.mean(np.array(result[i])))
        result_std.append(np.std(np.array(result[i]))) 
    
    result_mean[0], result_mean[2] = result_mean[2], result_mean[0]
    result_mean[0], result_mean[3] = result_mean[3], result_mean[0]
    result_std[0], result_std[2] = result_std[2], result_std[0]
    result_std[0], result_std[3] = result_std[3], result_std[0]
    plt.bar([0, 1, 2, 3, 4], result_mean, yerr=result_std, capsize=2)
    plt.xticks([0, 1, 2, 3, 4], ["Rank-4", "Rank-2", "Rank-1", "Rank-3", "Rank-5"])
    plt.ylabel("Selecting Time/s", size=12)
    plt.show()

if __name__ == "__main__":
    '''
    root = "./data-main/"
    users = utils.get_users("./data-main/")
    if os.path.exists("./select_time.txt"):
        os.remove("./select_time.txt")
    for user in users:
        if os.path.exists("./data-person/" + user + ".txt"):
            os.remove("./data-person/" + user + ".txt")
        select = [[], [], [], [], []]
        for i in range(5):
            if user == "wjs":
                continue
            print((user) )

            analyze_session_with_timestamp(root + user + "_" + str(i * 3) + ".txt", i * 3)
            analyze_session_with_timestamp(root + user + "_" + str(i * 3 + 1) + ".txt", i * 3 + 1)
            analyze_session_with_timestamp(root + user + "_" + str(i * 3 + 2) + ".txt", i * 3 + 2)

            if i > 0 and user in p_user:
                train(user, i * 3)
                combine_GP(user)
                test_selection(user, i * 3, True)
            else:
                test_selection(user, i * 3, False)
        with open("./select_time.txt", "a") as f:
            f.write(user + "\n")
            for j in range(5):
                f.write(str(np.mean(np.array(select[j]))) + " ")
            f.write("\n")
    '''
    draw_selection()

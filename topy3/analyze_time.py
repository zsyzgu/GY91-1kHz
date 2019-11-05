import utils
import sys
import os
from matplotlib import pyplot as plt
import numpy as np

p_word_length = [[], [], [], [], []]
p_typing_time = [[], [], [], [], []]
p_selecting_time = [[], [], [], [], []]
p_thinking_time = [[], [], [], [], []]
g_word_length = [[], [], [], [], []]
g_typing_time = [[], [], [], [], []]
g_selecting_time = [[], [], [], [], []]
g_thinking_time = [[], [], [], [], []]


p_user = ["gyz", "syt", "xcy", "ljs", "lw", "cwh", "wjs", "lsm"]
g_user = ["lzp", "xt", "xjj", "zzy", "lry", "lmm", "lq", "zwx"]

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

def analyze_session_with_timestamp(file, session):
    name = file.split('main/')[1].split("_")[0]
    output = open('./data-person/' + name + '.txt', 'a')

    task = []
    inputed = []
    inputed_letters = []
    word_buffer = []
    phrase_buffer = []
    time_buffer = []

    lines = [line.strip() for line in open(file, 'r').readlines()]
    for line in lines:
        tags = line.split()
        command = tags[1]
        if command == 'START_PHRASE':
            inputed = []
            time_buffer = []
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
                    word_buffer.append(tags[0] + ' ' + ' '.join(tags[2:]) + ' ' + letter)
        if command == 'ENTRY_A_WORD':
            if len(tags) == 3:
                inputed.append(tags[2])
                inputed_letters = []
                phrase_buffer.append(word_buffer)
                time_buffer.append(tags[0])
                word_buffer = []
            else:
                command = 'DELETE_LETTERS'
        if command == 'DELETE_A_WORD':
            if len(inputed) > 0:
                if len(inputed[-1]) == len(phrase_buffer[-1]):
                    output.write(inputed[-1] + ' ' + str(session) + ' ' + get_grams(task, len(inputed) - 1) + ' N\n')
                    for letter_info in phrase_buffer[-1]:
                        output.write(letter_info + '\n')
                    output.write(time_buffer[-1] + "\n")
                inputed.pop(-1)
                phrase_buffer.pop(-1)
                time_buffer.pop(-1)
                inputed_letters = []
                word_buffer = []
                if len(inputed) == 0:
                    inputed = []
                    phrase_buffer = []
                    time_buffer = []
        if command == 'DELETE_LETTERS':
            inputed_letters = []
            word_buffer = []
        if command == 'END_PHRASE':
            flag = (tags[2] == 'True') and (len(task) == len(inputed))
            if flag:
                for i in range(len(phrase_buffer)):
                    word_buffer = phrase_buffer[i]
                    time = time_buffer[i]
                    word = task[i]
                    is_correct = 'Y'
                    if inputed[i] != word:
                        is_correct = 'N'
                    if len(inputed[i]) == len(word):
                        output.write(word + ' ' + str(session) + ' ' + get_grams(task, i) + ' ' + is_correct + '\n')
                        for letter_info in word_buffer:
                            output.write(letter_info + '\n')
                        output.write(time + "\n")

def analyze_session():
    users = utils.get_users("./data-main")
    for user in users:
        if user == "wjs":
            continue
        print((user) )
        if os.path.exists("./data-time/" + user + ".txt"):
            os.remove("./data-time/" + user + ".txt")
        for f in os.listdir("./data-main/"):
            name = f.split("_")[0]
            session = int(f.split('_')[1].split('.')[0])
            if name == user:
                analyze_session_with_timestamp("./data-main/" + f, session)

def analyze_time():
    files = os.listdir("./data-time/")
    for index in range(5):
        for fs in files:
            if "result" in fs:
                continue
            word_len = []
            typing = []
            select = []
            thinking = []
            with open("./data-time/" + fs, "r") as f:
                lines = f.readlines()
                session = -1
                last_session = -1
                i = 0
                last = -1
                last_correct = ''
                last_gram = ''
                gram = ''
                while i < len(lines):
                    line = lines[i].strip().split()
                    session = int(line[1])
                    length = len(line[0])
                    correct = line[5]
                    gram = line[3]
                    if int(session / 3) == index and correct == "Y":
                        first_letter = float(int(lines[i + 1].strip().split()[0]) / 1e6)
                        last_letter = float(int(lines[i + length].strip().split()[0]) / 1e6)
                        selecting = float(int(lines[i + length + 1].strip().split()[0]) / 1e6)
                        word_len.append(length)
                        typing.append(last_letter - first_letter)
                        select.append(selecting - last_letter)
                        if last > 0 and session == last_session and correct == "Y" and correct == last_correct and first_letter > last and gram == last_gram:
                            if first_letter - last < 10:        
                                thinking.append(first_letter - last)
                        last = selecting
                    last_gram = line[0]
                    last_correct = correct
                    last_session = session
                    i += (length + 2)
            '''
            name = fs.split(".txt")[0]
            output = open("./data-time/" + name + "_result.txt", "a")
            output.write(str(np.mean(np.array(word_len))) + " " +
                        str(np.mean(np.array(typing))) + " " + 
                        str(np.mean(np.array(select))) + " " +
                        str(np.mean(np.array(thinking))) + "\n")
            '''
            g_word_length[index].append(np.mean(np.array(word_len)))
            g_typing_time[index].append(np.mean(np.array(typing)))
            g_selecting_time[index].append(np.mean(np.array(select)))
            g_thinking_time[index].append(np.mean(np.array(thinking)))
            
def draw_time():
    typing_mean = []
    typing_std = []
    selecting_mean = []
    selecting_std = []
    thinking_mean = []
    thinking_std = []
    for i in range(5):
        typing_mean.append(np.mean(np.array(g_typing_time[i])))
        typing_std.append(np.std(np.array(g_typing_time[i])))
        selecting_mean.append(np.mean(np.array(g_selecting_time[i])))
        selecting_std.append(np.std(np.array(g_selecting_time[i])))
        thinking_mean.append(np.mean(np.array(g_thinking_time[i])))
        thinking_std.append(np.std(np.array(g_thinking_time[i])))
    

    plt.errorbar([1, 2, 3, 4, 5], typing_mean, yerr=typing_std, elinewidth=2, capsize=4, color='gray', fmt='o')
    plt.errorbar([1, 2, 3, 4, 5], selecting_mean, yerr=selecting_std, elinewidth=2, capsize=4, color='orange', fmt='x')
    plt.errorbar([1, 2, 3, 4, 5], thinking_mean, yerr=thinking_std, elinewidth=2, capsize=4, color='skyblue')
    plt.plot([1, 2, 3, 4, 5], typing_mean, label='Typing', color='gray')
    plt.plot([1, 2, 3, 4, 5], selecting_mean, label='Selecting', color='orange')
    plt.plot([1, 2, 3, 4, 5], thinking_mean, label='Thinking', color='skyblue')
    plt.xlabel("Day", size=15)
    plt.ylabel("Time/s", size=15)
    plt.ylim(ymin=0, ymax=3)
    plt.legend(prop={'size': 15})
    plt.show()

if __name__ == "__main__":
    # analyze_session()
    analyze_time()
    draw_time()

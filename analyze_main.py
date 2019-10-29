import utils
import numpy as np
import sys

root = './data-main/'

def clac_uncorrected(A, B):
    n = len(A)
    m = len(B)
    F = np.zeros((n + 1) * (m + 1)).reshape(n + 1, m + 1)
    for i in range(1, n + 1):
        for j in range(i, m + 1):
            F[i, j] = max(F[i, j - 1], F[i - 1, j])
            if A[i - 1] == B[j - 1]:
                F[i, j] = max(F[i, j], F[i - 1, j - 1] + 1)
    return n - F[n, m]
    
def analyze_file(file):
    task_list = []
    duration_list = []
    inputed_list = []
    corrected_list = []

    lines = [line.strip() for line in open(file, 'r').readlines()]
    task = []
    start_timestamp = 0
    end_timestamp = 0
    is_started = False
    corrected = 0
    inputed = []
    for line in lines:
        tags = line.split()
        timestamp = int(tags[0])
        command = tags[1]
        if command == 'START_PHRASE':
            task = tags[2:]
            is_started = False
            corrected = 0
            inputed = []
        if command == 'ENTRY_A_LETTER':
            if is_started == False:
                is_started = True
                start_timestamp = timestamp
        if command == 'ENTRY_A_WORD':
            if len(tags) == 3:
                inputed.append(tags[2])
            end_timestamp = timestamp
        if command == 'DELETE_A_WORD':
            if len(inputed) > 0:
                inputed.pop(-1)
                corrected += 1
                if len(inputed) == 0:
                    is_started = False
                    corrected = 0
                    inputed = []
        if command == 'DELETE_LETTERS':
            if len(inputed) == 0:
                is_started = False
                corrected = 0
                inputed = []
        if command == 'END_PHRASE':
            flag = (tags[2] == 'True')
            if flag:
                task_list.append(task)
                duration_list.append(end_timestamp - start_timestamp)
                inputed_list.append(inputed)
                corrected_list.append(corrected)
    
    phrase_number = len(task_list)
    total_duration = 0
    total_CE = 0
    total_UCE = 0
    total_words = 0
    total_wpm_words = 0
    for i in range(phrase_number):
        task = task_list[i]
        inputed = inputed_list[i]
        duration = float(duration_list[i]) / 1000000
        corrected = corrected_list[i]
        wpm_words_number = float(len(''.join(task))) * 0.2
        wpm = wpm_words_number / (duration / 60)
        uncorrected = clac_uncorrected(task, inputed)
        '''
        print '(' + str(i) + ')', ' '.join(task)
        print 'WPM =', wpm
        print 'CE =', corrected
        print 'UCE =', uncorrected
        '''
        total_duration += duration
        total_CE += corrected
        total_UCE += uncorrected
        total_words += len(task)
        total_wpm_words += wpm_words_number
    print 'WPM =', float(total_wpm_words) / (total_duration / 60)
    print 'CER =', float(total_CE) / total_words
    print 'UCER =', float(total_UCE) / total_words
    return [float(total_wpm_words) / (total_duration / 60), float(total_CE) / total_words, float(total_UCE) / total_words]

def analyze_user(user, session=-1):
    if session == -1:
        file_names = utils.get_all_file_name(root + user + '_')
    else:
        file_names = utils.get_index_file_name(root + user + '_', session)
    for file in file_names:
        print file
        return analyze_file(file)
        # analyze_file(file)

if __name__ == "__main__":
    users = utils.get_users(root)
    session = -1
    if len(sys.argv) == 3:
        session = sys.argv[2]
    for user in users:
        analyze_user(user, session)

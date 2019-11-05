import sys
import os

def get_users(root):
    if (len(sys.argv) < 2):
        print( '[User] required.' )
        exit()
    user = sys.argv[1]
    users = []
    if user == '-A':
        for file in os.listdir(root):
            name = file.split('_')[0]
            if name not in users:
                users.append(name)
    else:
        users = user.split('_')
    return users

def get_next_file_name(prefix):
    trial = 0
    while True:
        file_name = prefix + str(trial) + '.txt'
        if not os.path.exists(file_name):
            break
        trial += 1
    return file_name, trial

def get_all_file_name(prefix):
    trial = 0
    file_names = []
    while True:
        file_name = prefix + str(trial) + '.txt'
        if not os.path.exists(file_name):
            break
        file_names.append(file_name)
        trial += 1
    return file_names

def get_index_file_name(prefix, index):
    file_name = prefix + str(index) + ".txt"
    if not os.path.exists(file_name):
        return []
    return [file_name]

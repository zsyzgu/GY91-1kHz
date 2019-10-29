import matplotlib.pyplot as plt
import numpy as np
import entry
import utils
import os
import math
from scipy.stats import linregress
from sklearn import linear_model

output = None

def read_data(file_name):
    layout = entry.Entry.layout
    data = []
    lines = open(file_name, 'r').readlines()

    last_row = None
    last_col = None
    last_heading = None
    buffer = []

    for line in lines:
        tags = line.strip().split()
        word = tags[-1]
        if word == 'Y' or word == 'N':
            if word == 'Y':
                data.extend(buffer)
            last_row = None
            last_col = None
            last_heading = None
            buffer = []
        elif word != '-' and word != '#':
            pitch = float(tags[10])
            heading = float(tags[11])
            word = str.lower(tags[-1])
            curr_row = layout[word][1]
            curr_col = layout[word][0]
            if last_col != None:
                row = layout[word][1]
                col = curr_col
                delta_heading = heading - last_heading
                buffer.append([row, col, last_row, last_col, pitch, delta_heading])
            last_row = curr_row
            last_col = curr_col
            last_heading = heading
    return data

def remove_bad_data(data):
    is_updated = False
    new_data = []

    row_dict = {}
    col_dict = {}

    for line in data:
        row = round(line[0], 1)
        pitch = line[4]
        delta_col = round(line[3] - line[1], 1)
        delta_heading = line[5]
        if not row_dict.has_key(row):
            row_dict[row] = []
        if not col_dict.has_key(delta_col):
            col_dict[delta_col] = []
        row_dict[row].append(pitch)
        col_dict[delta_col].append(delta_heading)
    
    for line in data:
        row = round(line[0], 1)
        pitch = line[4]
        delta_col = round(line[3] - line[1], 1)
        delta_heading = line[5]
        row_mean = np.mean(row_dict[row])
        row_std = np.std(row_dict[row])
        col_mean = np.mean(col_dict[delta_col])
        col_std = np.std(col_dict[delta_col])

        if abs(pitch - row_mean) <= 3 * row_std and abs(delta_heading - col_mean) <= 3 * col_std:
            new_data.append(line)
        else:
            is_updated = True

    if is_updated:
        return remove_bad_data(new_data)
    else:
        return new_data

def combine_data(X, Y):
    dict = {}

    for i in range(len(X)):
        if not dict.has_key(X[i]):
            dict[X[i]] = []
        dict[X[i]].append(Y[i])
    
    X = []
    Y = []

    for key, value in dict.items():
        X.append(key)
        Y.append(np.std(value))
    
    return X, Y

def output_model(data, person = None):
    if person == None:
        output = file('touch_model.m', 'w')
    else:
        output = file('./data-person/person_model_' + person + '.m', 'w')

    for i in range(26):
        ch = chr(ord('a') + i)
        r = entry.Entry.layout[ch][1]
        c = entry.Entry.layout[ch][0]
        Y = []
        for i in range(np.size(data, 0)):
            if abs(data[i, 0] - r) < 0.001 and abs(data[i, 1] - c) < 0.001:
                Y.append(data[i, 4])
        mean = 0
        std = 0
        if len(Y) <= 1:
            if r == 0: mean = entry.TouchModel.R0
            if r == 1: mean = entry.TouchModel.R1
            if r == 2: mean = entry.TouchModel.R2
            std = 0.05
        else:
            mean = np.mean(Y)
            std = np.std(Y)
        std = max(std, 0.05)
        samples = len(Y)
        output.write(str(mean) + ' ' + str(std) + ' ' + str(samples) + '\n')

    for r0 in range(3):
        for r1 in range(3):
            X = []
            Y = []
            for i in range(np.size(data, 0)):
                if abs(data[i, 2] - r0) < 0.001 and abs(data[i, 0] - r1) < 0.001:
                    X.append(round(data[i, 1] - data[i, 3], 1))
                    Y.append(data[i, 5])
            dict = {}

            for i in range(len(X)):
                if not dict.has_key(X[i]):
                    dict[X[i]] = []
                dict[X[i]].append(Y[i])

            for key, value in dict.items():
                if len(value) > 1:
                    mean = np.mean(value)
                    std = np.std(value)
                    std = max(std, 0.05)
                    samples = len(value)
                    output.write(str(r0) + ' ' + str(r1) + ' '  + str(key) + ' ' + str(mean) + ' ' + str(std) + ' ' + str(samples) + '\n')

def analyze_users(users):
    data = []
    for user in users:
        print user
        file_names = utils.get_all_file_name(root + user + '_')
        user_data = []
        for file_name in file_names:
            user_data.extend(read_data(file_name))
        user_data = remove_bad_data(user_data)
        data.extend(user_data)
    data = np.array(data).reshape(-1, 6)

    output_model(data)

def analyze_personal_users(users):
    for user in users:
        print user
        data = []
        file_names = utils.get_all_file_name(root + user + '_')
        user_data = []
        for file_name in file_names:
            user_data.extend(read_data(file_name))
        user_data = remove_bad_data(user_data)
        data.extend(user_data)
        data = np.array(data).reshape(-1, 6)
        output_model(data, user)

if __name__ == "__main__":
    root = './data-model/'
    users = utils.get_users(root)

    #analyze_users(users)
    analyze_personal_users(users)

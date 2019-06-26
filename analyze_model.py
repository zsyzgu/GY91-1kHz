import matplotlib.pyplot as plt
import numpy as np
import entry
import utils
import os
import math

output = file('touch_model.m', 'w')

def read_data(file_name):
    layout = entry.Entry.layout
    data = []
    lines = open(file_name, 'r').readlines()

    last_col = None
    last_heading = None
    buffer = []

    for line in lines:
        tags = line.strip().split()
        word = tags[-1]
        if word == 'Y' or word == 'N':
            if word == 'Y':
                data.extend(buffer)
            last_col = None
            last_heading = None
            buffer = []
        elif word != '-' and word != '#':
            pitch = float(tags[10])
            heading = float(tags[11])
            word = str.lower(tags[-1])
            curr_col = layout[word][0]
            if last_col != None:
                row = layout[word][1]
                col = curr_col
                delta_col = curr_col - last_col
                delta_heading = heading - last_heading
                buffer.append([row, col, pitch, delta_col, delta_heading])
            last_col = curr_col
            last_heading = heading
    return data

def remove_bad_samples(X):
    mean = np.mean(X)
    std = np.std(X)
    X_res = []
    for x in X:
        if (abs(x - mean) <= 3 * std):
            X_res.append(x)
    if len(X_res) == len(X):
        return X
    return remove_bad_samples(X_res)

def analyze_point_clouds(X, Y, is_result):
    X_res = []
    Y_res = []
    X_keys = []
    for i in range(len(X)):
        X[i] = round(X[i], 2)
        if X[i] not in X_keys:
            X_keys.append(X[i])
    X_keys.sort()
    for x in X_keys:
        values = []
        for i in range(len(X)):
            if (X[i] == x):
                values.append(Y[i])
        if is_result == False:
            values = remove_bad_samples(values)
        X_res.extend([x] * len(values))
        Y_res.extend(values)
        #X_res.extend([x])
        #Y_res.extend([np.mean(values)])
        if is_result and len(values) > 1:
            print 'X=', x, 'mean=', np.mean(values), 'std=', np.std(values), 'cnt=', len(values)
            output.write(str(x) + ' ' + str(np.mean(values)) + ' ' + str(np.std(values)) + '\n')
    #fit = np.polyfit(X_res, Y_res, 1)
    #print 'a=', fit[0], 'b=', fit[1], 'std =', np.std(values)
    if is_result == True:
        plt.plot(X_res, Y_res, '.')
        plt.show()
    return X_res, Y_res

if __name__ == "__main__":
    root = './data-model/'
    users = utils.get_users(root)

    X_row = []
    Y_row = []
    X_col = []
    Y_col = []
    for user in users:
        print user
        file_names = utils.get_all_file_name(root + user + '_')
        data = []
        for file_name in file_names:
            data.extend(read_data(file_name))
        data = np.array(data).reshape(-1, 5)

        rows = data[:, 1] # also x-axis: n.0, n.2, n.8 for the 1st, 2nd, 3st row
        cols = data[:, 1]
        pitchs = data[:, 2]
        delta_cols = data[:, 3]
        delta_headings = data[:, 4]

        # Pitch
        X, Y = analyze_point_clouds(rows, pitchs, False)
        X_row.extend(X)
        Y_row.extend(Y)

        # (Delta) Heading
        X, Y = analyze_point_clouds(delta_cols, delta_headings, False)
        X_col.extend(X)
        Y_col.extend(Y)
    
    print 'Total result:'
    output.write('Row\n')
    analyze_point_clouds(X_row, Y_row, True)
    output.write('Col\n')
    analyze_point_clouds(X_col, Y_col, True)
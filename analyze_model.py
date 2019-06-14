import matplotlib.pyplot as plt
import numpy as np
import entry
import utils
import os

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
            word = str.upper(tags[-1])
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

def analyze_point_clouds(X, Y, is_row, is_result):
    X_res = []
    Y_res = []
    X_keys = []
    for i in range(len(X)):
        X[i] = float(int(X[i] * 10)) / 10
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
        if is_row == True:
            print 'X=', x, 'Y=', np.mean(values), 'std=', np.std(values)
            if is_result == True:
                output.write(str(np.mean(values)) + ' ' + str(np.std(values)) + '\n')
    if is_row == False:
        fit = np.polyfit(X_res, Y_res, 1)
        values = [Y_res[i] - (fit[0] * X_res[i] + fit[1]) for i in range(len(X_res))]
        print 'a=', fit[0], 'b=', fit[1], 'std =', np.std(values)
        if is_result == True:
            output.write(str(fit[0]) + ' ' + str(fit[1]) + ' ' + str(np.std(values)) + '\n')
    plt.plot(X_res, Y_res, '.')
    #plt.show()
    return X_res, Y_res

if __name__ == "__main__":
    root = './data-model/'
    users = utils.get_users(root)

    X_row = []
    Y_row = []
    X_col = []
    Y_col = []
    for user in users:
        data = []
        trial = 0
        while True:
            file_name = root + user + '_' + str(trial) + '.txt'
            if not os.path.exists(file_name):
                break
            print file_name
            trial += 1
            data.extend(read_data(file_name))
        data = np.array(data).reshape(-1, 5)

        rows = data[:, 0]
        cols = data[:, 1]
        pitchs = data[:, 2]
        delta_cols = data[:, 3]
        delta_headings = data[:, 4]

        # Pitch
        X, Y = analyze_point_clouds(rows, pitchs, True, False)
        X_row.extend(X)
        Y_row.extend(Y)

        # (Delta) Heading
        X, Y = analyze_point_clouds(delta_cols, delta_headings, False, False)
        X_col.extend(X)
        Y_col.extend(Y)
    
    print 'Total result:'
    analyze_point_clouds(X_row, Y_row, True, True)
    analyze_point_clouds(X_col, Y_col, False, True)
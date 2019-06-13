import matplotlib.pyplot as plt
import numpy as np
import entry
import utils
import os

def read_data(file_name):
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

if __name__ == "__main__":
    root = './data-model/'
    users = utils.get_users(root)

    data = []
    for user in users:
        layout = entry.Entry.layout
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
    for i in range(3):
        row = np.array([pitchs[j] for j in range(len(rows)) if rows[j] == i])
        print 'row =', i, 'mean =', np.mean(row), 'std =', np.std(row)
    plt.plot(rows, pitchs, '.')
    plt.show()

    # (Delta) Heading
    print 'd_heading(d_col) =', np.poly1d(np.polyfit(delta_cols, delta_headings, 1))
    plt.plot(delta_cols, delta_headings, '.')
    plt.show()

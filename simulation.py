import entry
import utils

root = './data-model/'
layout = entry.Entry.layout

def analyze_file(file):
    lines = [line.strip() for line in open(file, 'r').readlines()]

    for line in lines:
        tags = line.split()

def analyze_user(user):
    file_names = utils.get_all_file_name(root + user + '_')
    for file_name in file_names:
        analyze_file(file_name)

users = utils.get_users(root)
for user in users:
    analyze_user(user)

'''
import matplotlib.pyplot as plt
import numpy as np

layout = {
    'Q':(0.0, 0), 'W':(1.0, 0), 'E':(2.0, 0), 'R':(3.0, 0), 'T':(4.0, 0), 'Y':(5.0, 0), 'U':(6.0, 0), 'I':(7.0, 0), 'O':(8.0, 0), 'P':(9.0, 0),
    'A':(0.2, 1), 'S':(1.2, 1), 'D':(2.2, 1), 'F':(3.2, 1), 'G':(4.2, 1), 'H':(5.2, 1), 'J':(6.2, 1), 'K':(7.2, 1), 'L':(8.2, 1),
    'Z':(0.8, 2), 'X':(1.8, 2), 'C':(2.8, 2), 'V':(3.8, 2), 'B':(4.8, 2), 'N':(5.8, 2), 'M':(6.8, 2)
}

def read_data(file_name, rows, cols, pitchs, delta_cols, delta_headings):
    lines = open(file_name, 'r').readlines()

    last_col = None
    last_heading = None

    for line in lines:
        tags = line.strip().split()

        if (tags[-1] != '-'):
            pitch = float(tags[10])
            heading = float(tags[11])
            word = tags[-1]
            curr_col = layout[word][0]
            if last_col != None:
                rows.append(layout[word][1])
                cols.append(curr_col)
                pitchs.append(pitch)
                delta_cols.append(curr_col - last_col)
                delta_headings.append(heading - last_heading)
            last_col = curr_col
            last_heading = heading
 
rows = []
cols = []
pitchs = []
delta_cols = []
delta_headings = []
read_data('p1.txt', rows, cols, pitchs, delta_cols, delta_headings)
read_data('p2.txt', rows, cols, pitchs, delta_cols, delta_headings)
read_data('p3.txt', rows, cols, pitchs, delta_cols, delta_headings)
read_data('p4.txt', rows, cols, pitchs, delta_cols, delta_headings)
read_data('p5.txt', rows, cols, pitchs, delta_cols, delta_headings)

# Pitch
# row = 0: mean = -0.4041, std = 0.0615
# row = 1: mean = -0.7298, std = 0.0608
# row = 2: mean = -1.0186, std = 0.0589
plt.plot(rows, pitchs, '.')
plt.show()

# (Delta) Heading
# delta_heading = -0.0544 * delta_cols - 0.0008 (std = 0.05397)
plt.plot(delta_cols, delta_headings, '.')
plt.show()
'''

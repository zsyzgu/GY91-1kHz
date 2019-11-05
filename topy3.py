import sys
import os

files = os.listdir('.')

for file in files:
    if file.split('.')[-1] == 'py':
        lines = open(file, 'r')
        output = open('./topy3/' + file, 'w')
        for line in lines:
            line = line.strip('\r\n')
            tags = line.split('print(') )
            if len(tags) == 2:
                line = tags[0] + 'print((' + tags[1] + ' )' )
            output.write(line + '\n')

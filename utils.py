import sys
import os

def get_users(root):
    if (len(sys.argv) != 2):
        print '[User] required.'
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

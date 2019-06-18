import utils

root = './data-main/'

def analyze_user(user):
    print user

users = utils.get_users(root)
for user in users:
    analyze_user(user)

import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate
import math
import random
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib
import sys
import os

def parse(file_name):
    inp = open(file_name, 'r')
    lines = inp.readlines()
    data = []
    for line in lines:
        tags = line.strip().split()
        frame = [float(tags[i]) for i in range(len(tags))]
        data.append(frame)
    return data

def caln_sequence(X):
    X = np.array(X)
    X_std = np.std(X)
    if (abs(X_std) < 0.001):
        return None
    X_min = np.min(X)
    X_max = np.max(X)
    X_mean = np.mean(X)
    X_sc = np.mean((X - X_mean) ** 3) / pow(X_std, 3)
    X_ku = np.mean((X - X_mean) ** 4) / pow(X_std, 4)
    return [X_mean, X_min, X_max, X_sc, X_ku]

def calc_feature(data):
    data = np.array(data).reshape(-1, 13)
    feature = []
    for i in range(1, 10):
        sequence = caln_sequence(data[:, i])
        if (sequence != None):
            feature.extend(sequence)
        else:
            return None
    return feature

def calc_positive_features(file_name):
    data = parse(file_name)
    last_tap_timestamp = 0
    features = []
    for i in range(1, len(data)):
        timestamp = int(data[i][0])
        if (data[i - 1][12] == 0 and data[i][12] == 1 and timestamp - last_tap_timestamp > 50 * 1000):
            last_tap_timestamp = timestamp
            feature = calc_feature(data[i - 30 : i + 20])
            if (feature != None):
                features.append(feature)
    return features

def calc_negative_features(file_name):
    data = parse(file_name)
    features = []
    cnt = 0
    while cnt < 167:
        j = random.randint(0, len(data) - 50) + 30
        feature = calc_feature(data[j - 30 : j + 20])
        if (feature != None):
            features.append(feature)
            cnt += 1
    return features

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print 'User name required.'
        exit()
    user = sys.argv[1]
    root = './data-contact/'

    X = []
    y = []
    for trial in range(10):
        file_name = root + user + '_p' + str(trial) + '.txt'
        if not os.path.exists(file_name):
            break
        positive_features = calc_positive_features(file_name)
        X.extend(positive_features)
        y.extend([1] * len(positive_features))
    print 'Positive samples = ' + str(len(X))

    for trial in range(10):
        file_name = root + user + '_n' + str(trial) + '.txt'
        if not os.path.exists(file_name):
            break
        negative_features = calc_negative_features(file_name)
        X.extend(negative_features)
        y.extend([0] * len(negative_features))
    print 'All samples = ' + str(len(X))

    clf = SVC(gamma='auto')
    clf.fit(X, y)
    scores = cross_val_score(clf, X, y, cv=10)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std()))
    joblib.dump(clf, "contact_model.m")

#clf = joblib.load("train_model.m")
#print clf.predict(X)

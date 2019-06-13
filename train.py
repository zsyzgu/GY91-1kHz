import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate
import math
import random
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib
import utils
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

def calc_features_from_positive(file_name):
    data = parse(file_name)
    last_tap_timestamp = 0
    positive_features = []
    negative_features = []
    for i in range(60, len(data) - 20):
        timestamp = int(data[i][0])
        if (data[i - 1][12] == 0 and data[i][12] == 1 and timestamp - last_tap_timestamp >= 100 * 1000):
            last_tap_timestamp = timestamp
            feature = calc_feature(data[i - 20 : i + 20])
            if (feature != None):
                positive_features.append(feature)
            feature = calc_feature(data[i - 60 : i - 20])
            if (feature != None):
                negative_features.append(feature)
    return positive_features, negative_features

def calc_features_from_negative(file_name):
    data = parse(file_name)
    features = []
    cnt = 0
    while cnt < 100:
        j = random.randint(0, len(data) - 20) + 20
        feature = calc_feature(data[j - 20 : j + 20])
        if (feature != None):
            features.append(feature)
            cnt += 1
    return features

if __name__ == "__main__":
    root = './data-contact/'
    users = utils.get_users(root)

    X = []
    y = []
    positive_samples = 0
    negative_samples = 0
    for user in users:
        for trial in range(10):
            file_name = root + user + '_p' + str(trial) + '.txt'
            if not os.path.exists(file_name):
                break
            positive_features, negative_features = calc_features_from_positive(file_name)
            X.extend(positive_features)
            y.extend([1] * len(positive_features))
            positive_samples += len(positive_features)
            X.extend(negative_features)
            y.extend([0] * len(negative_features))
            negative_samples += len(negative_features)

        for trial in range(10):
            file_name = root + user + '_n' + str(trial) + '.txt'
            if not os.path.exists(file_name):
                break
            negative_features = calc_features_from_negative(file_name)
            X.extend(negative_features)
            y.extend([0] * len(negative_features))
            negative_samples += len(negative_features)
    print 'Positive samples =', positive_samples
    print 'Negative samples =', negative_samples

    clf = SVC(gamma='auto')
    clf.fit(X, y)
    scores = cross_val_score(clf, X, y, cv=10)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std()))
    joblib.dump(clf, "contact_model.m")

#clf = joblib.load("train_model.m")
#print clf.predict(X)

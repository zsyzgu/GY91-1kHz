import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate
import math
import random
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib

class Contact:
    length = 40
    time_gap = 80
    suc_positive_threshold = 10

    clf = None
    data = []
    suc_positive = 0
    contact_cnt = 0

    def __init__(self):
        self.clf = joblib.load('contact_model.m')

    def update(self, nine_axis):
        if (len(self.data) >= self.length):
            self.data.pop(0)
        self.data.append(nine_axis)
        return self.is_contact()
    
    def caln_sequence(self, X):
        X_std = np.std(X)
        if (math.isnan(X_std) or abs(X_std) < 0.001):
            return None
        X_min = np.min(X)
        X_max = np.max(X)
        X_mean = np.mean(X)
        X_sc = np.mean((X - X_mean) ** 3) / pow(X_std, 3)
        X_ku = np.mean((X - X_mean) ** 4) / pow(X_std, 4)
        return [X_mean, X_min, X_max, X_sc, X_ku]

    def predict(self):
        if (len(self.data) != self.length):
            return False
        feature = []
        data = np.array(self.data).reshape(self.length, 9)
        for i in range(9):
            sequence = self.caln_sequence(data[:, i])
            if (sequence != None):
                feature.extend(sequence)
            else:
                return False
        if (self.clf.predict([feature])[0] == 1):
            return True
        return False
    
    def is_contact(self):
        result = False
        predict = self.predict()
        if (predict == True):
            self.suc_positive += 1
        else:
            self.suc_positive = 0
        if (self.suc_positive >= self.suc_positive_threshold):
            if (self.contact_cnt == 0):
                result = True
            self.contact_cnt = self.time_gap
        elif self.contact_cnt > 0:
            self.contact_cnt -= 1
        self.last_predict = predict
        return result


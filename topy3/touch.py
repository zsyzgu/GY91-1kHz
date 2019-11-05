from sklearn.externals import joblib
import numpy as np
import math
from sklearn import preprocessing
import time

class TouchUp:
    length = 40
    count = 0
    mean = []
    std = []
    time_cnt = 0
    time_cost = 0
    
    time = []
    time_delta = []
    up = []
    mo = []
    theta = []
    ax = []
    gz = []

    def __init__(self):
        self.clf = joblib.load("touchup_model.m")
        with open("./mean_std.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.split()
                self.mean.append(float(line[0]))
                self.std.append(float(line[1]))
    
    def update(self, data):
        if (len(self.ax) >= self.length):
            self.time.pop(0)
            self.up.pop(0)
            self.mo.pop(0)
            self.theta.pop(0)
            self.ax.pop(0)
            self.gz.pop(0)
        self.time.append(int(data[0]))
        nine_axis = data[1 : 10]
        self.ax.append(nine_axis[3])
        self.gz.append(nine_axis[2])
        mo_temp = nine_axis[3] * nine_axis[3] + nine_axis[4] * nine_axis[4] + nine_axis[5] * nine_axis[5]
        up_temp = nine_axis[3] * nine_axis[6] + nine_axis[4] * nine_axis[7] + nine_axis[5] * nine_axis[8]
        acc = (mo_temp) ** 0.5
        self.up.append(up_temp)
        self.mo.append(mo_temp)
        self.theta.append((up_temp) / (acc))
    
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

    def predict(self, last_tapping):
        if (len(self.ax) != self.length):
            return False
        time_delta = []
        feature = []
        for i in range(len(self.time)):
            time_delta.append(self.time[i] - last_tapping)
        data = [time_delta, self.ax, self.gz, self.up, self.mo, self.theta]
        for i in range(6):
            sequence = self.caln_sequence(data[i])
            if (sequence != None):
                feature.extend(sequence)
            else:
                return False
        for i in range(len(feature)):
            feature[i] = (feature[i] - self.mean[i]) / self.std[i]
        temp = self.clf.predict([feature])[0]
        if temp == 1:
            return True
        return False

    def is_touchup(self, last_tapping):
        predict = self.predict(last_tapping)
        if predict == True:
            self.count += 1
        else:
            self.count = 0
        if self.count == 5:
            return True
        else:
            return False

from sklearn.externals import joblib
import numpy as np
import math
from sklearn import preprocessing
import time

class TouchUp:
    length = 40
    data = []
    count = 0
    mean = []
    std = []
    time_cnt = 0
    time_cost = 0

    def __init__(self):
        self.clf = joblib.load("touchup_model.m")
        with open("./mean_std.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.split()
                self.mean.append(float(line[0]))
                self.std.append(float(line[1]))
    
    def update(self, data):
        if (len(self.data) >= self.length):
            self.data.pop(0)
        self.data.append(data)
    
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
        if (len(self.data) != self.length):
            return False
        feature = []
        data = []
        time_delta = []
        up = []
        mo = []
        theta = []
        ax = []
        gz = []
        for i in range(len(self.data)):
            time_delta.append(int(self.data[i][0]) - last_tapping)
            nine_axis = self.data[i][1 : 10]
            ax.append(nine_axis[3])
            gz.append(nine_axis[2])
            mo_temp = nine_axis[3] * nine_axis[3] + nine_axis[4] * nine_axis[4] + nine_axis[5] * nine_axis[5]
            up_temp = nine_axis[3] * nine_axis[6] + nine_axis[4] * nine_axis[7] + nine_axis[5] * nine_axis[8]
            acc = (mo_temp) ** 0.5
            up.append(up_temp)
            mo.append(mo_temp)
            theta.append((up_temp) / (acc))

        data = [time_delta, ax, gz, up, mo, theta]

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
        if self.count == 10:
            return True
        else:
            return False

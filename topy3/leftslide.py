from sklearn.externals import joblib
import numpy as np
import math

class LeftSlide:
    length = 80
    data = []
    count = 0

    def __init__(self):
        self.clf = joblib.load("leftslide_model.m")
    
    def update(self, nine_axis):
        if (len(self.data) >= self.length):
            self.data.pop(0)
        self.data.append(nine_axis)
    
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
        data = np.array(self.data).reshape(self.length, 11)
        for i in range(11):
            sequence = self.caln_sequence(data[:, i])
            if (sequence != None):
                feature.extend(sequence)
            else:
                return False
        if (self.clf.predict([feature])[0] == 1):
            return True
        return False

    def is_leftslide(self):
        predict = self.predict()
        return predict
        if predict == True:
            self.count += 1
        else:
            self.count = 0
        if self.count == 1:
            return True
        else:
            return False

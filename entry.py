import numpy as np
import math

class Entry:
    row_mean = [-0.5, -0.8, -1.1]
    row_std = [0.1, 0.1, 0.1]
    col_a = -0.05
    col_b = 0.00
    col_std = 0.1
    layout = {
        'Q':(0.0, 0), 'W':(1.0, 0), 'E':(2.0, 0), 'R':(3.0, 0), 'T':(4.0, 0), 'Y':(5.0, 0), 'U':(6.0, 0), 'I':(7.0, 0), 'O':(8.0, 0), 'P':(9.0, 0),
        'A':(0.2, 1), 'S':(1.2, 1), 'D':(2.2, 1), 'F':(3.2, 1), 'G':(4.2, 1), 'H':(5.2, 1), 'J':(6.2, 1), 'K':(7.2, 1), 'L':(8.2, 1),
        'Z':(0.8, 2), 'X':(1.8, 2), 'C':(2.8, 2), 'V':(3.8, 2), 'B':(4.8, 2), 'N':(5.8, 2), 'M':(6.8, 2)
    }
    word_number = 3000
    words = []
    words_freq = []

    def __init__(self, word_number = 3000):
        self.word_number = word_number
        lines = open('corpus.txt', 'r').readlines()[:word_number]
        self.words = [str.upper(line.strip().split()[0]) for line in lines]
        self.words_freq = [int(line.strip().split()[1]) for line in lines]
        self.load_touch_model()

    def load_touch_model(self):
        lines = [line.strip().split() for line in open('touch_model.m', 'r').readlines()]
        self.row_mean[0] = float(lines[0][0])
        self.row_mean[1] = float(lines[1][0])
        self.row_mean[2] = float(lines[2][0])
        self.row_std[0] = float(lines[0][1])
        self.row_std[1] = float(lines[1][1])
        self.row_std[2] = float(lines[2][1])
        self.col_a = float(lines[3][0])
        self.col_b = float(lines[3][1])
        self.col_std = float(lines[3][2])
        print 'Touch Model:', lines

    def calc_scores(self, pitchs, headings):
        scores = []
        for i in range(len(self.words)):
            length = len(self.words[i])
            if length != len(pitchs):
                scores.append(-1e6)
                continue
            score = math.log(self.words_freq[i])
            # Pitch
            # row = 0: mean = -0.4041, std = 0.0615
            # row = 1: mean = -0.7298, std = 0.0608
            # row = 2: mean = -1.0186, std = 0.0589
            for j in range(length):
                row = self.layout[self.words[i][j]][1]
                mean = self.row_mean[row]
                std = self.row_std[row]
                score += -math.log(std) - 0.5 * ((pitchs[j] - mean) / std) ** 2
                #score += -((pitchs[j] - mean) / std) ** 2
            # Heading
            # delta_heading = -0.0544 * delta_cols - 0.0008 (std = 0.05397)
            for j in range(1, length):
                delta_col = self.layout[self.words[i][j]][0] - self.layout[self.words[i][j - 1]][0]
                mean = self.col_a * delta_col + self.col_b
                std = self.col_std
                score += -math.log(std) - 0.5 * ((headings[j] - headings[j - 1] - mean) / std) ** 2
                #score += -((headings[j] - headings[j - 1] - mean) / std) ** 2
            scores.append(score)
        return scores
    
    def predict(self, pitchs, delta_headings):
        candidates = []
        scores = self.calc_scores(pitchs, delta_headings)

        for i in range(5):
            id = scores.index(max(scores))
            if (scores[id] <= -1e6):
                candidates.append('')
            else:
                candidates.append(self.words[id])
            scores[id] = -1e6
        
        return candidates

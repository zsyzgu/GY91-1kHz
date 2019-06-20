import numpy as np
import math
import scipy.io as io

class Entry:
    row_mean = [-0.5, -0.8, -1.1]
    row_std = [0.1, 0.1, 0.1]
    col_a = -0.05
    col_b = 0.00
    col_std = 0.1
    layout = {
        'q':(0.0, 0), 'w':(1.0, 0), 'e':(2.0, 0), 'r':(3.0, 0), 't':(4.0, 0), 'y':(5.0, 0), 'u':(6.0, 0), 'i':(7.0, 0), 'o':(8.0, 0), 'p':(9.0, 0),
        'a':(0.2, 1), 's':(1.2, 1), 'd':(2.2, 1), 'f':(3.2, 1), 'g':(4.2, 1), 'h':(5.2, 1), 'j':(6.2, 1), 'k':(7.2, 1), 'l':(8.2, 1),
        'z':(0.8, 2), 'x':(1.8, 2), 'c':(2.8, 2), 'v':(3.8, 2), 'b':(4.8, 2), 'n':(5.8, 2), 'm':(6.8, 2)
    }
    word_number = 3000
    words = []
    words_freq = []
    use_bigrams = False
    bigrams = None
    last_word_id = 0

    def __init__(self, word_number = 3000):
        self.word_number = word_number
        self.load_corpus(word_number)
        self.load_bigrams(word_number)
        self.load_touch_model()

    def load_corpus(self, word_number):
        lines = open('corpus.txt', 'r').readlines()[:word_number]
        self.words = [str.lower(line.strip().split()[0]) for line in lines]
        self.words_freq = [int(line.strip().split()[1]) for line in lines]
    
    def load_bigrams(self, word_number):
        if word_number <= 5000:
            self.use_bigrams = True
            if word_number <= 3000:
                self.bigrams = io.loadmat('bigrams-3000')['mat']
            else:
                self.bigrams = io.loadmat('bigrams-5000')['mat']
            print 'Language Model = Bigrams'
            return
        print 'Language Model = Unigram'

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
    
    def update_last_word(self, word):
        if self.use_bigrams == True:
            self.last_word_id = 0
            if word == None:
                return
            word = str.lower(word)
            for i in range(len(self.words)):
                if word == self.words[i]:
                    self.last_word_id = i + 1
                    break

    def calc_scores(self, pitchs, headings):
        scores = []
        for i in range(len(self.words)):
            length = len(self.words[i])
            if length != len(pitchs):
                scores.append(-1e6)
                continue
            score = 0
            if self.use_bigrams == False: # Unigram
                score = math.log(self.words_freq[i])
            else: # Bigrams
                score = math.log(self.bigrams[self.last_word_id, i + 1])

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

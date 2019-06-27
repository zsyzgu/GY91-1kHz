import numpy as np
import math
import scipy.io as io

class TouchModel:
    row_pc = {}
    col_pc = {}
    col_a = 0
    col_b = 0
    col_std = 0

    def __init__(self):
        lines = [line.strip().split() for line in open('touch_model.m', 'r').readlines()]
        split_id = 0
        for i in range(len(lines)):
            if lines[i][0] == 'Col':
                split_id = i
        X = []
        Y = []
        STD = []
        for i in range(1, len(lines)):
            if i == split_id:
                continue
            x = float(lines[i][0])
            mean = float(lines[i][1])
            std = float(lines[i][2])
            if i < split_id:
                self.row_pc[x] = [mean, std]
            else:
                self.col_pc[x] = [mean, std]
                X.append(x)
                Y.append(mean)
                STD.append(std)
        fit = np.polyfit(X, Y, 1)
        self.col_a = fit[0]
        self.col_b = fit[1]
        self.col_std = np.mean(STD)
    
    def calc_row_score(self, col, pitch):
        [mean, std] = self.row_pc[col] # col = n.0, n.2, n.8 stand for the 1st, 2nd, 3st rows
        return -math.log(std) - 0.5 * ((pitch - mean) / std) ** 2
    
    def calc_col_score(self, delta_col, delta_heading):
        if self.col_pc.has_key(delta_col):
            [mean, std] = self.col_pc[delta_col]
        else:
            mean = self.col_a * delta_col + self.col_b
            std = self.col_std
        return -math.log(std) - 0.5 * ((delta_heading - mean) / std) ** 2
    
    def calc_score(self, word, pitchs, headings):
        score = 0
        for i in range(len(word)): # Pitch
            score += self.calc_row_score(Entry.layout[word[i]][0], pitchs[i])
        for i in range(1, len(word)): # Heading
            score += self.calc_col_score(round(Entry.layout[word[i]][0] - Entry.layout[word[i - 1]][0], 2), headings[i] - headings[i - 1])
        return score

class LanguageModel:
    USE_UNITGRAM = 0
    USE_BIGRAMS = 1
    USE_TRIGRAMS = 2

    word_number = 3000
    LM = USE_UNITGRAM
    words = []
    unitgram = None
    bigrams = None
    trigrams = None
    last_word_id = 0

    def __init__(self, word_number = 3000, LM = USE_UNITGRAM):
        if word_number > 5000:
            LM = self.USE_UNITGRAM
        
        self.word_number = word_number
        self.LM = LM

        if LM == self.USE_UNITGRAM:
            print 'Language Model = Unigram'
        if LM == self.USE_BIGRAMS:
            print 'Language Model = Bigrams'
        if LM == self.USE_TRIGRAMS:
            print 'Language Model = Trigrams'
        
        assert LM >= self.USE_UNITGRAM
        self.load_unitgram()

        if LM >= self.USE_BIGRAMS and word_number <= 5000:
            self.load_bigrams()

        if LM >= self.USE_TRIGRAMS and word_number <= 5000:
            self.load_trigrams()

    def load_unitgram(self):
        lines = open('corpus.txt', 'r').readlines()[:self.word_number]
        self.words = [str.lower(line.strip().split()[0]) for line in lines]
        self.unitgram = np.array([float(line.strip().split()[1]) for line in lines])
        self.unitgram /= sum(self.unitgram)
    
    def load_bigrams(self):
        self.bigrams = io.loadmat('bigrams-5000')['mat']
    
    def load_trigrams(self):
        self.trigrams = io.loadmat('trigrams-5000')['mat']
    
    def calc_score(self, id):
        score = 0
        if self.LM >= self.USE_BIGRAMS and self.last_word_id != 0 and self.bigrams[self.last_word_id, id + 1] != 0: # Bigrams
            score = math.log(self.bigrams[self.last_word_id, id + 1])
        else: # Unigram
            score = math.log(self.unitgram[id])
        return score

class Entry:
    MAX_CANDIDATES = 5
    touch_model = None
    language_model = None
    words = []
    layout = {
        'q':(0.0, 0), 'w':(1.0, 0), 'e':(2.0, 0), 'r':(3.0, 0), 't':(4.0, 0), 'y':(5.0, 0), 'u':(6.0, 0), 'i':(7.0, 0), 'o':(8.0, 0), 'p':(9.0, 0),
        'a':(0.2, 1), 's':(1.2, 1), 'd':(2.2, 1), 'f':(3.2, 1), 'g':(4.2, 1), 'h':(5.2, 1), 'j':(6.2, 1), 'k':(7.2, 1), 'l':(8.2, 1),
        'z':(0.8, 2), 'x':(1.8, 2), 'c':(2.8, 2), 'v':(3.8, 2), 'b':(4.8, 2), 'n':(5.8, 2), 'm':(6.8, 2)
    }

    def __init__(self, word_number = 3000, use_bigrams = True):
        self.word_number = word_number
        self.touch_model = TouchModel()
        self.language_model = LanguageModel(word_number, LanguageModel.USE_BIGRAMS)
        self.words = self.language_model.words
    
    def update_last_word(self, word):
        if self.language_model.LM >= LanguageModel.USE_BIGRAMS:
            self.language_model.last_word_id = 0
            if word == None:
                return
            word = str.lower(word)
            for i in range(len(self.words)):
                if word == self.words[i]:
                    self.language_model.last_word_id = i + 1
                    break

    def calc_scores(self, pitchs, headings):
        scores = []
        for i in range(len(self.words)):
            length = len(self.words[i])
            if length != len(pitchs):
                scores.append(-1e6)
                continue
            score = self.language_model.calc_score(i) + self.touch_model.calc_score(self.words[i], pitchs, headings)
            scores.append(score)
        return scores
    
    def predict(self, pitchs, headings):
        candidates = []
        scores = self.calc_scores(pitchs, headings)

        for i in range(self.MAX_CANDIDATES):
            id = scores.index(max(scores))
            if (scores[id] <= -1e6):
                candidates.append('')
            else:
                candidates.append(self.words[id])
            scores[id] = -1e6
        
        return candidates

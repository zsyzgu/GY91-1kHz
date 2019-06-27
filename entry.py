import numpy as np
import math
import scipy.io as io

class TouchModel:
    R0 = -0.49
    R1 = -0.78
    R2 = -1.03

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
        [mean, std] = [0, 0]
        if self.row_pc.has_key(col):
            [mean, std] = self.row_pc[col] # col = n.0, n.2, n.8 stand for the 1st, 2nd, 3st rows
        else:
            if (abs(col - math.floor(col) - 0.0) < 0.01):
                [mean, std] = [self.R0, 0.1]
            if (abs(col - math.floor(col) - 0.2) < 0.01):
                [mean, std] = [self.R1, 0.1]
            if (abs(col - math.floor(col) - 0.8) < 0.01):
                [mean, std] = [self.R2, 0.1]
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
    word_ids = {}
    unitgram = None
    bigrams = None
    trigrams = None
    gram_1 = 0
    gram_2 = 0
    prepared_trigrams = None

    def __init__(self, word_number = 3000, LM = USE_BIGRAMS):
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
        self.word_ids['<S>'] = 0
        for i in range(len(self.words)):
            self.word_ids[self.words[i]] = i + 1
    
    def load_bigrams(self):
        self.bigrams = io.loadmat('bigrams-5000')['mat']
    
    def load_trigrams(self):
        self.trigrams = io.loadmat('trigrams-5000')['mat']
    
    def calc_score(self, id):
        score = 0
        if self.LM >= self.USE_TRIGRAMS and self.gram_1 != 0 and self.gram_2 != 0 and self.prepared_trigrams[id] != 0: # Trigrams
            score = math.log(self.prepared_trigrams[id])
        elif self.LM >= self.USE_BIGRAMS and self.gram_1 != 0 and self.bigrams[self.gram_1, id + 1] != 0: # Bigrams
            score = math.log(self.bigrams[self.gram_1, id + 1])
        else: # Unigram
            score = math.log(self.unitgram[id])
        return score
    
    def prepare_trigrams(self):
        if self.LM >= self.USE_TRIGRAMS and self.gram_1 != 0 and self.gram_2 != 0:
            self.prepared_trigrams = np.zeros(self.word_number)
            L = 0
            R = np.size(self.trigrams, 0)
            while L < R:
                mid = int((L + R) / 2)
                if self.trigrams[mid][0] > self.gram_2 or (self.trigrams[mid][0] == self.gram_2 and self.trigrams[mid][1] >= self.gram_1):
                    R = mid
                else:
                    L = mid + 1
            i = L
            while i < np.size(self.trigrams, 0) and self.trigrams[i][0] == self.gram_2 and self.trigrams[i][1] == self.gram_1:
                id = int(self.trigrams[i][2] - 1)
                if id < self.word_number:
                    self.prepared_trigrams[id] = self.trigrams[i][3]
                i += 1

    def update_grams(self, gram_1, gram_2):
        self.gram_1 = 0
        self.gram_2 = 0
        if gram_1 != None and self.word_ids.has_key(gram_1):
            self.gram_1 = self.word_ids[gram_1]
        if gram_2 != None and self.word_ids.has_key(gram_2):
            self.gram_2 = self.word_ids[gram_2]

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

    def __init__(self, word_number = 3000, LM = LanguageModel.USE_BIGRAMS):
        self.word_number = word_number
        self.touch_model = TouchModel()
        self.language_model = LanguageModel(word_number, LM)
        self.words = self.language_model.words

    def update_grams(self, gram_1, gram_2):
        if self.language_model.LM >= LanguageModel.USE_BIGRAMS:
            self.language_model.update_grams(gram_1, gram_2)

    def calc_scores(self, pitchs, headings):
        self.language_model.prepare_trigrams()
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

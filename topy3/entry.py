import numpy as np
import math
import scipy.io as io
import time

class TouchModel:
    R0 = -0.52
    R1 = -0.81
    R2 = -1.03

    def __init__(self, person = None):
        self.pitch_data = []
        self.heading_data = []
        file = 'touch_model.m'
        if person != None:
            file = './data-person/touch_model_' + person + '.m'
        lines = [line.strip().split() for line in open(file, 'r').readlines()]
        for i in range(0, 26):
            self.pitch_data.append([float(v) for v in lines[i]])
        self.heading_data = [None] * 200
        for i in range(26, len(lines)):
            line = [float(v) for v in lines[i]]
            id = int((line[0] * 3 + line[1]) * 20 + line[2] + 10)
            self.heading_data[id] = [line[3], line[4]]
    
    def calc_pitch_score(self, letter, pitch):
        id = ord(letter) - ord('a')
        mean = self.pitch_data[id][0]
        std = self.pitch_data[id][1]
        return -math.log(std) - 0.5 * ((pitch - mean) / std) ** 2
    
    def calc_heading_score(self, last_row, row, delta_col, delta_heading):
        mean = -0.05 * delta_col
        std = 0.05
        id = int((last_row * 3 + row) * 20 + delta_col + 10)
        tags = self.heading_data[id]
        if tags != None:
            mean = tags[0]
            std = tags[1]
        return -math.log(std) - 0.5 * ((delta_heading - mean) / std) ** 2
    
    def calc_score(self, word, pitchs, headings):
        score = 0
        last_row = None
        last_col = None
        for i in range(len(word)):
            row = Entry.layout[word[i]][1]
            col = Entry.layout[word[i]][0]
            score += self.calc_pitch_score(word[i], pitchs[i]) # Pitch
            if last_row != None:
                score += self.calc_heading_score(last_row, row, col - last_col, headings[i] - headings[i - 1]) # Heading
            last_row = row
            last_col = col
        return score

class LanguageModel:
    USE_UNITGRAM = 0
    USE_BIGRAMS = 1
    USE_TRIGRAMS = 2

    '''
    unitgram = None
    bigrams = None
    trigrams = None
    gram_1 = 0
    gram_2 = 0
    bigrams_data = None
    trigrams_data = None
    '''

    def __init__(self, word_number = 3000, LM = USE_BIGRAMS):
        if word_number > 10000:
            LM = self.USE_UNITGRAM
        
        self.word_number = word_number
        self.LM = LM

        if LM == self.USE_UNITGRAM:
            print( 'Language Model = Unigram' )
        if LM == self.USE_BIGRAMS:
            print( 'Language Model = Bigrams' )
        if LM == self.USE_TRIGRAMS:
            print( 'Language Model = Trigrams' )
        
        assert LM >= self.USE_UNITGRAM
        self.load_unitgram()

        if LM >= self.USE_BIGRAMS:
            self.load_bigrams()

        if LM >= self.USE_TRIGRAMS:
            self.load_trigrams()

    def load_unitgram(self):
        lines = open('corpus.txt', 'r').readlines()[:self.word_number]
        self.words = [str.lower(line.strip().split()[0]) for line in lines]
        self.unitgram = np.array([float(line.strip().split()[1]) for line in lines])
        self.unitgram /= sum(self.unitgram)
        self.word_ids = {}
        self.word_ids['<S>'] = 0
        for i in range(len(self.words)):
            self.word_ids[self.words[i]] = i + 1
    
    def load_bigrams(self):
        if self.word_number <= 5000:
            self.bigrams_data = io.loadmat('bigrams-5000')['mat']
        else:
            self.bigrams_data = io.loadmat('bigrams-10000')['mat']
    
    def load_trigrams(self):
        if self.word_number <= 5000:
            self.trigrams_data = io.loadmat('trigrams-5000')['mat']
            self.trigrams_size = 5000
        else:
            self.trigrams_data = io.loadmat('trigrams-10000')['mat']
            self.trigrams_size = 10000
    
    def calc_score(self, id):
        score = 0
        if self.LM >= self.USE_TRIGRAMS and self.gram_1 != 0 and self.gram_2 != 0 and self.trigrams[id] != 0: # Trigrams
            score = math.log(self.trigrams[id])
        elif self.LM >= self.USE_BIGRAMS and self.gram_1 != 0 and self.bigrams[id] != 0: # Bigrams
            score = math.log(self.bigrams[id])
        else: # Unigram
            score = math.log(self.unitgram[id])
        return score

    def prepare_bigrams(self):
        if self.LM >= self.USE_BIGRAMS and self.gram_1 != 0:
            self.bigrams = self.bigrams_data[self.gram_1, 1 : self.word_number + 1]
            self.bigrams /= sum(self.bigrams)

    def prepare_trigrams(self):
        if self.LM >= self.USE_TRIGRAMS and self.gram_1 != 0 and self.gram_2 != 0:
            self.trigrams = np.zeros(self.word_number)
            L = 0
            R = np.size(self.trigrams_data, 0)
            gram_id = self.gram_2 * (self.trigrams_size + 1) + self.gram_1
            while L < R:
                mid = int((L + R) / 2)
                if self.trigrams_data[mid][0] >= gram_id:
                    R = mid
                else:
                    L = mid + 1
            i = L
            
            total = 0
            data_size = np.size(self.trigrams_data, 0)
            while i < data_size and self.trigrams_data[i][0] == gram_id:
                id = int(self.trigrams_data[i][1] - 1)
                if id < self.word_number:
                    self.trigrams[id] = self.trigrams_data[i][2]
                    total += self.trigrams_data[i][2]
                i += 1
            
            if total > 0:
                self.trigrams /= total

    def update_grams(self, gram_1, gram_2):
        self.gram_1 = 0
        self.gram_2 = 0
        if gram_1 != None and self.word_ids.has_key(gram_1):
            self.gram_1 = self.word_ids[gram_1]
        if gram_2 != None and self.word_ids.has_key(gram_2):
            self.gram_2 = self.word_ids[gram_2]

class Entry:
    MAX_CANDIDATES = 5
    layout = {
        'q':(0.0, 0), 'w':(1.0, 0), 'e':(2.0, 0), 'r':(3.0, 0), 't':(4.0, 0), 'y':(5.0, 0), 'u':(6.0, 0), 'i':(7.0, 0), 'o':(8.0, 0), 'p':(9.0, 0),
        'a':(0.2, 1), 's':(1.2, 1), 'd':(2.2, 1), 'f':(3.2, 1), 'g':(4.2, 1), 'h':(5.2, 1), 'j':(6.2, 1), 'k':(7.2, 1), 'l':(8.2, 1),
        'z':(0.8, 2), 'x':(1.8, 2), 'c':(2.8, 2), 'v':(3.8, 2), 'b':(4.8, 2), 'n':(5.8, 2), 'm':(6.8, 2)
    }

    def __init__(self, word_number = 3000, LM = LanguageModel.USE_BIGRAMS, person = None):
        self.word_number = word_number
        self.touch_model = TouchModel(person)
        self.language_model = LanguageModel(word_number, LM)
        self.words = self.language_model.words

    def update_grams(self, gram_1, gram_2):
        if self.language_model.LM >= LanguageModel.USE_BIGRAMS:
            self.language_model.update_grams(gram_1, gram_2)

    def calc_scores(self, pitchs, headings):
        self.language_model.prepare_bigrams()
        self.language_model.prepare_trigrams()
        scores = []
        pitchs_len = len(pitchs)
        words_len = len(self.words)
        for i in range(words_len):
            length = len(self.words[i])
            if length != pitchs_len:
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

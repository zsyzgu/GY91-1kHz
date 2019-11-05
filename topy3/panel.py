from cv2 import cv2
import numpy as np
import threading
import time
import random
import entry

class HeadingVsPitch:  # Only update selection bar when d(heading)>d(pitch) in the past 31 ms
    HISTORY_LEN = 100
    tot = 0
    history = [0] * HISTORY_LEN

    def __init__(self):
        self.reset(0, 0)
    
    def reset(self, heading, pitch):
        self.length = 31
        self.last_heading = heading
        self.last_pitch = pitch
        self.tot = 0
        self.cnt = 0
        self.queue = [0] * self.length
    
    def update(self, heading, pitch):
        curr_status = int(abs(heading - self.last_heading) > abs(pitch - self.last_pitch))
        self.cnt = self.cnt - self.queue[self.tot % self.length] + curr_status
        self.queue[self.tot % self.length] = curr_status
        self.tot += 1
        self.last_heading = heading
        self.last_pitch = pitch

    def is_heading_significant(self):
        return self.cnt > min(self.tot, self.length) * 0.5
    
    def start_selection(self):
        self.tot = 0

    def update_selecting(self, selecting):
        self.history[self.tot % self.HISTORY_LEN] = int(selecting)
        self.tot += 1
    
    def get_selecting(self):
        if self.tot < self.HISTORY_LEN:
            return self.history[0]
        return self.history[(self.tot + 1) % self.HISTORY_LEN]

class Panel:
    running = False
    updated = False
    length = 50 # Pixels of a key
    image = np.zeros((5 * length + 1, 10 * length + 1, 3), np.uint8)
    layout = entry.Entry.layout
    phrase_cnt = 0
    phrases = []
    entry = None
    heading_vs_pitch = HeadingVsPitch()

    # Keyboard
    visual_row = None

    # Candidate bar
    start_heading = 0
    candidates = []
    selecting = None
    candidate_rank = [3, 1, 0, 2, 4]

    # Text bar
    text_task = ''
    text_inputed = ''

    def __init__(self, entry = None):
        self.running = True
        thread = threading.Thread(target = self.update)
        thread.start()

        phrases = [str.lower(line.strip()) for line in open('phrases-main.txt', 'r').readlines()]
        if entry == None:
            self.phrases = phrases
        else:
            self.entry = entry
            for phrase in phrases:
                words = phrase.split()
                flag = True
                for word in words:
                    if str.lower(word) not in entry.words:
                        flag = False
                if flag == True:
                    self.phrases.append(phrase)
            print( 'Words number =', len(entry.words) )
            print( 'Phrases number =', len(self.phrases) )
        random.shuffle(self.phrases)
        
        self.show_keyboard()
        self.redo_phrase()
        self.update_candidates_bar()

    def update(self):
        cv2.imshow('image', self.image)
        while self.running:
            if self.updated:
                cv2.imshow('image', self.image)
                self.updated = False
            cv2.waitKey(5)
    
    def stop(self):
        self.running = False
        cv2.destroyAllWindows()
    
    # Keyboard

    def show_keyboard(self):
        for i in range(26):
            ch = chr(i + ord('a'))
            if self.layout.has_key(ch):
                pos = self.layout[ch]
                cv2.rectangle(self.image, (int(pos[0] * self.length), int((pos[1] + 2) * self.length)), (int((pos[0] + 1) * self.length), int((pos[1] + 3) * self.length)), (255, 255, 255), 1)
                cv2.putText(self.image, str.upper(ch), (int(pos[0] * self.length) + 15, int((pos[1] + 3) * self.length) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)            
        self.updated = True

    def update_visual_row(self, pitch):
        row = None
        if pitch != None:
            if (pitch < entry.TouchModel.R1):
                row = 1 + (pitch - entry.TouchModel.R1) / (entry.TouchModel.R2 - entry.TouchModel.R1)
            else:
                row = 1 - (pitch - entry.TouchModel.R1) / (entry.TouchModel.R0 - entry.TouchModel.R1)
            row = float(int((row + 1) * 5)) / 5 - 1
            if row < -0.5 or row > 2.5:
                row = None
        if self.visual_row != row:
            self.visual_row = row
            cv2.rectangle(self.image, (0, 2 * self.length - 1), (10 * self.length, 5 * self.length - 1), (0, 0, 0), -1)
            if row != None:
                cv2.line(self.image, (0, int((2.5 + row) * self.length)), (10 * self.length, int((2.5 + row) * self.length)), (128, 128, 128), 1)
            self.show_keyboard()

    # Text bar

    def update_text_bar(self):
        cv2.rectangle(self.image, (0, 0), (10 * self.length, self.length - 1), (0, 0, 0), -1)
        cv2.putText(self.image, self.text_task, (int(self.length * 0.5), int(self.length * 0.4)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(self.image, self.text_inputed, (int(self.length * 0.5), int(self.length * 0.8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        self.updated = True

    def update_text_task(self, str):
        self.text_task = str
        self.update_text_bar()
    
    def update_text_inputed(self, str):
        self.text_inputed = str
        self.update_text_bar()
    
    def next_phrase(self):
        self.phrase_cnt += 1
        self.text_task = self.phrases[self.phrase_cnt]
        self.text_inputed = ''
        self.update_text_bar()
        if self.entry != None:
            self.entry.update_grams(None, None)
    
    def redo_phrase(self):
        self.text_task = self.phrases
        self.text_task = self.phrases[self.phrase_cnt]
        self.text_inputed = ''
        self.update_text_bar()
        if self.entry != None:
            self.entry.update_grams(None, None)
    
    def text_next_word(self):
        length = len(self.text_inputed)
        if length >= len(self.text_task):
            self.update_text_inputed(self.text_inputed + '#')
            return '#'
        word = self.text_task[length]
        if word == ' ':
            self.text_inputed += ' '
            return self.text_next_word()
        self.update_text_inputed(self.text_inputed + word)
        return word
    
    def find_grams(self):
        if len(self.text_inputed) == 0:
            self.entry.update_grams(None, None)
            return
        num = len(self.text_inputed.split(' '))
        tags = self.text_task.split(' ')
        gram_1 = None
        gram_2 = None
        if 0 <= num - 1 and num - 1 < len(tags):
            gram_1 = tags[num - 1]
        if 0 <= num - 2 and num - 2 < len(tags):
            gram_2 = tags[num - 2]
        self.entry.update_grams(gram_1, gram_2)

    def text_add_word(self, str):
        if (len(self.text_inputed) > 0) and len(str) > 0:
            self.text_inputed += ' '
        self.text_inputed += str
        self.update_text_bar()
        if self.entry != None:
            self.find_grams()
    
    def text_delete_word(self):
        if (len(self.text_inputed) > 0):
            self.text_inputed = ' '.join(self.text_inputed.split(' ')[:-1])
            self.update_text_bar()
        if self.entry != None:
            self.find_grams()

    # Candidate bar

    def update_candidates_bar(self):
        candidates = self.candidates
        selecting = self.selecting
        for i in range(5):
            cv2.rectangle(self.image, (i * 2 * self.length + 1, self.length), ((i + 1) * 2 * self.length - 1, 2 * self.length - 1), (0, 0, 0), 1)
            if self.selecting != None and i == int(self.selecting):
                cv2.rectangle(self.image, (i * 2 * self.length + 1, self.length), ((i + 1) * 2 * self.length - 1, 2 * self.length - 1), (64, 64, 64), -1)
            else:
                cv2.rectangle(self.image, (i * 2 * self.length + 1, self.length), ((i + 1) * 2 * self.length - 1, 2 * self.length - 1), (32, 32, 32), -1)
        if selecting != None:
            cv2.line(self.image, (int(selecting * 2 * self.length), self.length + 1), (int(selecting * 2 * self.length),  2 * self.length - 2), (128, 128, 128), 1)
        for i in range(5):
            id = self.candidate_rank[i]
            if (id < len(candidates)):
                candidate = str.lower(candidates[id])
                font_size = 0.6
                if (len(candidate) >= 8):
                    font_size = 4.8 / len(candidate)
                cv2.putText(self.image, candidate, (int(i * 2 * self.length) + 5, 2 * self.length - 10), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), 1)
        self.updated = True

    def update_candidates(self, candidates):
        self.candidates = candidates
        self.update_candidates_bar()
    
    def start_selection(self, heading, pitch):
        self.heading_vs_pitch.reset(heading, pitch)
        self.start_heading = heading
        self.selecting = 2.5
        self.update_candidates_bar()
        self.heading_vs_pitch.start_selection()
    
    def update_selection(self, heading, pitch):
        self.heading_vs_pitch.update(heading, pitch)
        selecting = 2.5 + (heading - self.start_heading) / (-0.05)
        selecting = int(selecting * 5) / 5.0 + 0.1
        self.heading_vs_pitch.update_selecting(selecting)
        if self.heading_vs_pitch.is_heading_significant() and selecting != self.selecting: # Only update when d(heading)>d(pitch) in the past 31 ms
            self.selecting = selecting
            self.update_candidates_bar()

    def clear_candidates_bar(self):
        self.selecting = None
        self.candidates = []
        self.update_candidates_bar()

    def get_selecting_candidate(self):
        select = self.heading_vs_pitch.get_selecting() # The selection 100 ms before
        if (0 <= select and select < 5):
            id = self.candidate_rank[select]
            if (id < len(self.candidates)):
                return str.lower(self.candidates[id])
        return ''

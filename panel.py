import cv2
import numpy as np
import threading
import time
import random
import entry

class Panel:
    running = False
    updated = False
    length = 50 # Pixels of a key
    image = np.zeros((5 * length + 1, 10 * length + 1, 3), np.uint8)
    layout = entry.Entry.layout
    phrase_cnt = 0
    phrases = [line.strip() for line in open('phrases.txt', 'r').readlines()]
    random.shuffle(phrases)

    # Keyboard
    visual_row = None

    # Candidate bar
    candidates = None
    selected = None
    candidate_rank = [3, 1, 0, 2, 4]

    # Text bar
    text_task = ''
    text_inputed = ''

    def __init__(self):
        self.running = True
        thread = threading.Thread(target = self.run)
        thread.start()

        self.show_keyboard()
        self.redo_phrase()
    
    def run(self):
        cv2.imshow('image', self.image)
        while self.running:
            if self.updated:
                cv2.imshow('image', self.image)
                self.updated = False
            cv2.waitKey(10)
    
    def stop(self):
        self.running = False
        cv2.destroyAllWindows()
    
    # Keyboard

    def show_keyboard(self):
        for i in range(26):
            ch = chr(i + ord('A'))
            if self.layout.has_key(ch):
                pos = self.layout[ch]
                cv2.rectangle(self.image, (int(pos[0] * self.length), int((pos[1] + 2) * self.length)), (int((pos[0] + 1) * self.length), int((pos[1] + 3) * self.length)), (255, 255, 255), 1)
                cv2.putText(self.image, ch, (int(pos[0] * self.length) + 15, int((pos[1] + 3) * self.length) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)            
        self.updated = True

    def update_visual_row(self, pitch):
        row = None
        if pitch != None:
            row_mean = entry.Entry.row_mean
            if (pitch < row_mean[1]):
                row = 1 + (pitch - row_mean[1]) / (row_mean[2] - row_mean[1])
            else:
                row = 1 - (pitch - row_mean[1]) / (row_mean[0] - row_mean[1])
            row = float(int((row + 1) * 5)) / 5 - 1
            if row < -0.5 or row > 2.5:
                row = None
        if self.visual_row != row:
            self.visual_row = row
            cv2.rectangle(self.image, (0, 2 * self.length - 1), (10 * self.length, 5 * self.length - 1), (0, 0, 0), -1)
            if row != None:
                cv2.line(self.image, (0, int((2.5 + row) * self.length)), (10 * self.length, int((2.5 + row) * self.length)), (64, 64, 64), 1)
            self.show_keyboard()

    # Text bar

    def update_text_bar(self):
        cv2.rectangle(self.image, (0, 0), (10 * self.length, self.length - 1), (0, 0, 0), -1)
        cv2.putText(self.image, self.text_task, (int(self.length * 0.5), int(self.length * 0.4)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(self.image, self.text_inputed, (int(self.length * 0.5), int(self.length * 0.8)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
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
    
    def redo_phrase(self):
        self.text_task = self.phrases
        self.text_task = self.phrases[self.phrase_cnt]
        self.text_inputed = ''
        self.update_text_bar()
    
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
    
    def text_add_word(self, str):
        if (len(self.text_inputed) > 0) and len(str) > 0:
            self.text_inputed += ' '
        self.text_inputed += str
        self.update_text_bar()
    
    def text_delete_word(self):
        if (len(self.text_inputed) > 0):
            self.text_inputed = ' '.join(self.text_inputed.split(' ')[:-1])
            self.update_text_bar()

    # Candidate bar

    def update_candidates_bar(self):
        candidates = self.candidates
        selected = self.selected
        cv2.rectangle(self.image, (0, self.length), (10 * self.length, 2 * self.length - 1), (0, 0, 0), -1)
        if selected != None:
            cv2.rectangle(self.image, (int(selected) * 2 * self.length, self.length), ((int(selected) + 1) * 2 * self.length, 2 * self.length - 1), (64, 64, 64), -1)
            cv2.line(self.image, (int(selected * 2 * self.length), self.length + 1), (int(selected * 2 * self.length),  2 * self.length - 2), (0, 0, 0), 2)
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
    
    def update_selected(self, selected):
        selected = int(selected * 5) / 5.0 + 0.1
        if selected != self.selected:
            self.selected = selected
            self.update_candidates_bar()

    def clear_candidates_bar(self):
        self.candidates = []
        self.selected = None
        self.update_candidates_bar()

    def get_selected_candidate(self):
        select = int(self.selected)
        if (0 <= select and select < 5):
            id = self.candidate_rank[select]
            if (id < len(self.candidates)):
                return str.lower(self.candidates[id])
        return ''
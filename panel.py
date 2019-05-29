import cv2
import numpy as np
import threading
import time
import random

class Panel:
    running = False
    updated = False
    length = 50 # Pixels of a key
    image = np.zeros((5 * length + 1, 10 * length + 1, 3), np.uint8)
    layout = {
        'Q':(0.0, 0), 'W':(1.0, 0), 'E':(2.0, 0), 'R':(3.0, 0), 'T':(4.0, 0), 'Y':(5.0, 0), 'U':(6.0, 0), 'I':(7.0, 0), 'O':(8.0, 0), 'P':(9.0, 0),
        'A':(0.2, 1), 'S':(1.2, 1), 'D':(2.2, 1), 'F':(3.2, 1), 'G':(4.2, 1), 'H':(5.2, 1), 'J':(6.2, 1), 'K':(7.2, 1), 'L':(8.2, 1),
        'Z':(0.8, 2), 'X':(1.8, 2), 'C':(2.8, 2), 'V':(3.8, 2), 'B':(4.8, 2), 'N':(5.8, 2), 'M':(6.8, 2)
    }
    phrase_cnt = 0
    phrases = [line.strip() for line in open('phrases.txt', 'r').readlines()]
    random.shuffle(phrases)

    # Candidate bar
    candidates = None
    selected = None
    candidate_rank = [3, 1, 0, 2, 4]

    # Text bar
    text_task = ''
    text_inputed = ''

    def __init__(self):
        for i in range(26):
            ch = chr(i + ord('A'))
            if self.layout.has_key(ch):
                pos = self.layout[ch]
                cv2.rectangle(self.image, (int(pos[0] * self.length), int((pos[1] + 2) * self.length)), (int((pos[0] + 1) * self.length), int((pos[1] + 3) * self.length)), (255, 255, 255), 1)

        self.running = True
        thread = threading.Thread(target = self.run)
        thread.start()
    
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

    def show_words(self):
        for i in range(26):
            ch = chr(ord('A') + i)
            color = (255, 255, 255)
            pos = self.layout[ch]
            cv2.putText(self.image, ch, (int(pos[0] * self.length) + 15, int((pos[1] + 3) * self.length) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        self.updated = True

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
                cv2.putText(self.image, str.lower(candidates[id]), (int(i * 2 * self.length) + 5, 2 * self.length - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
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
        elif select < 0:
            return '[delete]'
        return ''

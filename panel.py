import cv2
import numpy as np
import threading
import time

class Panel:
    running = False
    updated = False
    last_ch = None
    length = 50
    candidates = None
    selected = None
    candidate_rank = [3, 1, 0, 2, 4]

    layout = {
        'Q':(0.0, 0), 'W':(1.0, 0), 'E':(2.0, 0), 'R':(3.0, 0), 'T':(4.0, 0), 'Y':(5.0, 0), 'U':(6.0, 0), 'I':(7.0, 0), 'O':(8.0, 0), 'P':(9.0, 0),
        'A':(0.2, 1), 'S':(1.2, 1), 'D':(2.2, 1), 'F':(3.2, 1), 'G':(4.2, 1), 'H':(5.2, 1), 'J':(6.2, 1), 'K':(7.2, 1), 'L':(8.2, 1),
        'Z':(0.8, 2), 'X':(1.8, 2), 'C':(2.8, 2), 'V':(3.8, 2), 'B':(4.8, 2), 'N':(5.8, 2), 'M':(6.8, 2)
    }

    image = np.zeros((5 * length + 1, 10 * length + 1, 3), np.uint8)

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
    
    def draw_word(self, ch, color):
        pos = self.layout[ch]
        cv2.putText(self.image, ch, (int(pos[0] * self.length) + 15, int((pos[1] + 3) * self.length) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    def update_word(self, ch):
        if not (ord('A') <= ord(ch) and ord(ch) <= ord('Z')):
            return
        if (self.last_ch != None):
            self.draw_word(self.last_ch, (0, 0, 0))
        self.draw_word(ch, (255, 255, 255))
        self.updated = True
        self.last_ch = ch
    
    def show_words(self):
        for i in range(26):
            self.draw_word(chr(ord('A') + i), (255, 255, 255))
        self.updated = True

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

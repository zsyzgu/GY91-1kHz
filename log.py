import os
import sys
import utils

class Log:
    output = None
    timestamp = 0

    def __init__(self):
        root = './data-main/'
        user = utils.get_users(root)[0]
        file_name, trial = utils.get_next_file_name(root + user + '_')
        print 'Block', trial, 'begin.'
        self.output = open(file_name, 'w')

    def log_raw_data(self, data):
        self.timestamp = int(data[0])
        self.output.write(' '.join([str(v) for v in data]) + '\n')

    def start_phrase(self, task):
        self.output.write(str(self.timestamp) + ' START_PHRASE ' + task + '\n')
    
    def end_phrase(self, accepted):
        self.output.write(str(self.timestamp) + ' END_PHRASE ' + str(accepted) + '\n')
    
    def entry_a_word(self, word):
        self.output.write(str(self.timestamp) + ' ENTRY_A_WORD ' + word + '\n')
    
    def delete_a_word(self):
        self.output.write(str(self.timestamp) + ' DELETE_A_WORD' + '\n')

    def entry_a_letter(self, pitch, heading):
        self.output.write(str(self.timestamp) + ' ENTRY_A_LETTER ' + str(pitch) + ' ' + str(heading) + '\n')
        
    def delete_letters(self):
        self.output.write(str(self.timestamp) + ' DELETE_LETTERS' + '\n')

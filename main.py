import read_serial
import oscilloscope
import keyboard
import panel
import pygame
import entry
import time
import math
import event
import log

log = log.Log()
entry = entry.Entry(5000, entry.LanguageModel.USE_TRIGRAMS)
input = read_serial.ReadSerial()
input.get_data()
pan = panel.Panel(entry)
log.start_phrase(pan.text_task)
print 'Trial', pan.phrase_cnt, 'begin.'

pitchs = []
headings = []
event = event.Event()

def clear():
    global pitchs
    global headings
    global pan
    pitchs = []
    headings = []
    pan.clear_candidates_bar()
    pan.update_visual_row(None)

T = 0
down_pitch = 0.0
down_heading = 0.0

while True:
    T += 1
    if T % 10 == 0 and (keyboard.is_pressed('q') or pan.phrase_cnt == 10):
        break
    if T % 10 == 5 and len(pan.text_inputed) > 0:
        if keyboard.is_pressed('y'): # Next phrase
            log.end_phrase(True)
            pan.next_phrase()
            log.start_phrase(pan.text_task)
            clear()
            print 'Trial', pan.phrase_cnt, 'begin.'
        elif keyboard.is_pressed('n'): # Redo the phrase
            log.end_phrase(False)
            pan.redo_phrase()
            log.start_phrase(pan.text_task)
            clear()
    data = input.get_data() # [t, gx, gy, gz, ax, ay, az, gra_x, gra_y, gra_z, pitch, heading, is_touch]
    log.log_raw_data(data)

    timestamp = data[0]
    pitch = data[10]
    heading = data[11]

    curr_event = event.get_event(data)
    if curr_event == event.SLIDE_LEFT: # Deletion
        if len(pitchs) == 0: # Delete a word
            pan.text_delete_word()
            log.delete_a_word()
        else: # Delete letters
            log.delete_letters()
        clear()

    if len(pan.candidates) >= 1 and pan.selecting == None and curr_event == event.LONG_PRESS: # Trigger Selection
        pan.start_selection(heading, pitch)
    
    if pan.selecting != None:
        pan.update_selection(heading, pitch)
    
    if curr_event == event.TOUCH_DOWN:
        down_pitch = pitch
        down_heading = heading
    
    if curr_event == event.TOUCH_UP: # Confirm
        if pan.selecting == None: # Typing
            # pan.update_visual_row(down_pitch) # Visual feedback
            pitchs.append(down_pitch)
            headings.append(down_heading)
            candidates = entry.predict(pitchs, headings)
            pan.update_candidates(candidates)
            log.entry_a_letter(down_pitch, down_heading)
        else: # Selection
            word = pan.get_selecting_candidate()
            pan.text_add_word(word)
            clear()
            if word == '':
                log.delete_letters()
            else:
                log.entry_a_word(word)

pan.stop()
time.sleep(1)

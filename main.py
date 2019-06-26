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

'''
input = read_serial.ReadSerial()
ev = event.Event()
while True:
    if keyboard.is_pressed('q'):
        break
    data = input.get_data() # [t, gx, gy, gz, ax, ay, az, gra_x, gra_y, gra_z, pitch, heading, is_touch]
    curr_event = ev.get_event(data)
exit()
'''

log = log.Log()
input = read_serial.ReadSerial()
input.get_data()
entry = entry.Entry(3000)
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

while True:
    if keyboard.is_pressed('q') or pan.phrase_cnt == 10:
        break
    if len(pan.text_inputed) > 0:
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
    nine_axis = data[1 : 10]
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

    if curr_event == event.TOUCH_UP: # Confirm
        if pan.selecting == None: # Typing
            if keyboard.is_pressed('s'):
                pan.update_visual_row(pitch)
            pitchs.append(pitch)
            headings.append(heading)
            candidates = entry.predict(pitchs, headings)
            pan.update_candidates(candidates)
            log.entry_a_letter(pitch, heading)
        else: # Selection
            word = pan.get_selecting_candidate()
            pan.text_add_word(word)
            clear()
            log.entry_a_word(word)

pan.stop()
time.sleep(1)

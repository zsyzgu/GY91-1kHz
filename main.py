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
input = read_serial.ReadSerial()
input.get_data()
entry = entry.Entry(3000)
pan = panel.Panel(entry)
log.start_phrase(pan.text_task)

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

while True:
    if keyboard.is_pressed('q'):
        break
    if len(pan.text_inputed) > 0:
        if keyboard.is_pressed('y'): # Next phrase
            log.end_phrase(True)
            pan.next_phrase()
            log.start_phrase(pan.text_task)
            clear()
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

    event_touch_down, event_long_press, event_long_idle = event.get_event(data)
    
    if event_long_press: # Trigger Deletion
        if len(pitchs) <= 1: # Delete a word
            pan.text_delete_word()
            log.delete_a_word()
        else: # Delete letters
            log.delete_letters()
        clear()
    
    if event_long_idle and len(pitchs) > 0 and pan.selecting == None: # Trigger Selection
        pan.start_selection(heading, pitch)

    if pan.selecting != None: # Maintain Selection
        pan.update_selection(heading, pitch)
        pan.update_visual_row(None)

    if event_touch_down:
        if pan.selecting == None: # Entry Letter
            pan.update_visual_row(pitch)
            pitchs.append(pitch)
            headings.append(heading)
            candidates = entry.predict(pitchs, headings)
            pan.update_candidates(candidates)
            log.entry_a_letter(pitch, heading)
        else: # Select Candidate
            word = pan.get_selecting_candidate()
            pan.text_add_word(word)
            clear() # Close Selection
            log.entry_a_word(word)

pan.stop()
time.sleep(1)

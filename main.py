import read_serial
import oscilloscope
import keyboard
import panel
import pygame
import entry
import time
import math
import event

input = read_serial.ReadSerial()
input.get_data()
pan = panel.Panel()
entry = entry.Entry(10000)

pitchs = []
headings = []
select_heading = None
event = event.Event()

while True:
    if keyboard.is_pressed('q'):
        break
    if len(pan.text_inputed) > 0:
        if keyboard.is_pressed('y'): # Next phrase
            pan.next_phrase()
        elif keyboard.is_pressed('n'): # Redo the phrase
            pan.redo_phrase()
    data = input.get_data() # [t, gx, gy, gz, ax, ay, az, gra_x, gra_y, gra_z, pitch, heading, is_touch]

    timestamp = data[0]
    nine_axis = data[1 : 10]
    pitch = data[10]
    heading = data[11]

    event_touch_down, event_long_press, event_long_idle = event.get_event(timestamp, nine_axis)
    
    if event_long_press: # Trigger Deletion
        if len(pitchs) <= 1: # Delete the word (if not: delete letters)
            pan.text_delete_word()
        pitchs = []
        headings = []
        pan.clear_candidates_bar()
    
    if event_long_idle and len(pitchs) > 0 and pan.selected == None: # Trigger Selection
        select_heading = heading
        pan.update_selected(2.5)

    if pan.selected != None:
        selected = 2.5 - (heading - select_heading) / 0.1
        pan.update_selected(selected)
        pan.update_visual_row(None)

    if event_touch_down:
        if pan.selected == None: # Entry Word
            pan.update_visual_row(pitch)
            pitchs.append(pitch)
            headings.append(heading)
            candidates = entry.predict(pitchs, headings)
            pan.update_candidates(candidates)
        else: # Select Candidate
            word = pan.get_selected_candidate()
            pan.text_add_word(word)
            pitchs = []
            headings = []
            pan.clear_candidates_bar()

pan.stop()

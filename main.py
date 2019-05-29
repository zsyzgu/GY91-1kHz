import read_serial
import oscilloscope
import keyboard
import contact
import panel
import pygame
import entry
import time
import math

input = read_serial.ReadSerial()
input.get_data()
cont = contact.Contact()
pan = panel.Panel()
pan.show_words()
pan.redo_phrase()
entry = entry.Entry(10000)

pitchs = []
headings = []
select_heading = None
idle = 0

while True:
    if keyboard.is_pressed('q'):
        break
    if len(pan.text_inputed) > 0:
        if keyboard.is_pressed('y'): # Next phrase
            pan.next_phrase()
        elif keyboard.is_pressed('n'): # Redo the phrase
            pan.redo_phrase()
    data = input.get_data() # [t, gx, gy, gz, ax, ay, az, gra_x, gra_y, gra_z, pitch, heading, is_touch]
    nine_axis = data[1 : 10]
    pitch = data[10]
    heading = data[11]

    if data[4] ** 2 + data[5] ** 2 + data[6] ** 2 <= 0.2 ** 2:
        idle += 1
    else:
        idle = 0

    if idle >= 400 and len(pitchs) > 0 and pan.selected == None: # Trigger Selection
        select_heading = heading
        pan.update_selected(2.5)
    
    if pan.selected != None:
        selected = 2.5 - (heading - select_heading) / 0.1
        pan.update_selected(selected)

    if (cont.update(nine_axis) == True):
        if pan.selected == None: # Entry Word
            pitchs.append(pitch)
            headings.append(heading)
            candidates = entry.predict(pitchs, headings)
            pan.update_candidates(candidates)
        else: # Select Candidate
            word = pan.get_selected_candidate()
            if word == '[delete]':
                pan.text_delete_word()
            else:
                pan.text_add_word(word)
            pitchs = []
            headings = []
            pan.clear_candidates_bar()

pan.stop()

import read_serial
import oscilloscope
import keyboard
import contact
import panel
import pygame
import os
import time
import sys

if (len(sys.argv) != 2):
    print '[User] required.'
    exit()
name = sys.argv[1]
trial = 0
while True:
    file_name = './data-model/' + name + '_' + str(trial) + '.txt'
    if not os.path.exists(file_name):
        break
    trial += 1

input = read_serial.ReadSerial()
data = input.get_data()
print 'Block ' + str(trial) + ' begin.'

output = open(file_name, 'w')
cont = contact.Contact()
pan = panel.Panel()
pygame.mixer.init()  
pygame.mixer.music.load("prompt.mp3")
print 'Trial ' + str(pan.phrase_cnt) + ' begin.'

while True:
    if keyboard.is_pressed('q') or pan.phrase_cnt >= 10:
        break
    
    data = input.get_data() #[t, gx, gy, gz, ax, ay, az, gra_x, gra_y, gra_z, pitch, heading, is_touch]
    line = ' '.join([str(v) for v in data])
    remark = '-'

    if len(pan.text_inputed) > 0:
        if keyboard.is_pressed('y'): # Next phrase
            pan.next_phrase()
            remark = 'Y'
            print 'Trial ' + str(pan.phrase_cnt) + ' begin.'
        elif keyboard.is_pressed('n'): # Redo the phrase
            pan.redo_phrase()
            remark = 'N'
            print 'Trial ' + str(pan.phrase_cnt) + ' begin.'

    if (cont.update(data[1 : 10]) == True):
        pygame.mixer.music.play()
        pygame.mixer.music.play()
        remark = pan.text_next_word()
    
    output.write(line + ' ' + remark + '\n')

pan.stop()
time.sleep(0.5)

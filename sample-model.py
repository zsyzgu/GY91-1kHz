import read_serial
import oscilloscope
import keyboard
import contact
import panel
import pygame

input = read_serial.ReadSerial()
output = open('p.txt', 'w')
cont = contact.Contact()
pan = panel.Panel()
pan.show_words()
pan.redo_phrase()
pygame.mixer.init()  
pygame.mixer.music.load("prompt.mp3")

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
        elif keyboard.is_pressed('n'): # Redo the phrase
            pan.redo_phrase()
            remark = 'N'

    if (cont.update(data[1 : 10]) == True):
        pygame.mixer.music.play()
        pygame.mixer.music.play()
        remark = pan.text_next_word()
        print remark
    
    output.write(line + ' ' + remark + '\n')

pan.stop()

import read_serial
import oscilloscope
import keyboard
import contact
import panel
import pygame

input = read_serial.ReadSerial()
output = open('p.txt', 'w')
cont = contact.Contact()
task = str.upper(''.join([line.strip().split()[0] for line in open('lexicon.txt', 'r').readlines()]))
cnt = 0
pan = panel.Panel()
pan.update_word(task[0])
pygame.mixer.init()  
pygame.mixer.music.load("prompt.mp3")

while True:
    if keyboard.is_pressed('q') or cnt >= 500:
        break
    data = input.get_data() #[t, gx, gy, gz, ax, ay, az, gra_x, gra_y, gra_z, pitch, heading, is_touch]
    line = ' '.join([str(v) for v in data])
    
    if (cont.update(data[1 : 10]) == True):
        print data[0]
        pygame.mixer.music.play()
        pygame.mixer.music.play()
        line = line + ' ' + task[cnt]
        cnt += 1
        pan.update_word(task[cnt])
    else:
        line = line + ' -'
    
    output.write(line + '\n')

pan.stop()

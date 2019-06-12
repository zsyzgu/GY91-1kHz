import read_serial
import oscilloscope
import keyboard
import contact
import panel
import os
import sys

if (len(sys.argv) != 3):
    print '[User] and [p/n] required.'
    exit()
name = sys.argv[1] + '_' + sys.argv[2]
trial = 0
while True:
    file_name = './data-contact/' + name + str(trial) + '.txt'
    if not os.path.exists(file_name):
        break
    trial += 1

input = read_serial.ReadSerial()
data = input.get_data()
print 'Trial ' + str(trial) + ' begin.'

output = open(file_name, 'w')
last_is_touch = 0
last_tap_timestamp = 0
cnt = 0
samples = 100

while True:
    if keyboard.is_pressed('q') or cnt == samples:
        break
    data = input.get_data() #[t, gx, gy, gz, ax, ay, az, gra_x, gra_y, gra_z, pitch, heading, is_touch]
    output.write(' '.join([str(v) for v in data]) + '\n')
    is_touch = int(data[-1])
    timestamp = int(data[0])
    if is_touch == 1 and last_is_touch == 0 and timestamp - last_tap_timestamp >= 100 * 1000:
        cnt += 1
        print str(cnt) + ' / ' + str(samples)
        last_tap_timestamp = timestamp
    last_is_touch = is_touch

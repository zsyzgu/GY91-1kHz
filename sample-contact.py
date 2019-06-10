import read_serial
import oscilloscope
import keyboard
import contact
import panel

input = read_serial.ReadSerial()
output = open('n_lwq3.txt', 'w')

for i in range(100000):
    if keyboard.is_pressed('q'):
        break
    data = input.get_data() #[t, gx, gy, gz, ax, ay, az, gra_x, gra_y, gra_z, pitch, heading, is_touch]
    output.write(' '.join([str(v) for v in data]) + '\n')
    print data[0]

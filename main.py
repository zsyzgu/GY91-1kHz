import read_serial
import oscilloscope
import keyboard

osc = oscilloscope.Oscilloscope()
input = read_serial.ReadSerial()

for i in range(50000):
    if keyboard.is_pressed('q'):
        break
    [t, gx, gy, gz, ax, ay, az, gra_x, gra_y, gra_z, pitch, heading] = input.get_data()
    osc.append_data([pitch, heading])
    print heading

osc.stop()

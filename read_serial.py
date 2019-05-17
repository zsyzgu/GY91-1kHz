import serial
import time
import madgwickahrs

ser = serial.Serial('COM5', 250000)
time.sleep(0.1)
ser.read(ser.in_waiting)
mad = madgwickahrs.MadgwickAHRS()

start_time = time.time()

fout = open('data.txt', 'w')

def read_buf(data, offset):
    x = ord(data[offset + 1]) * 256 + ord(data[offset])
    if x >= 32768:
        x -= 65536
    return x

for i in range(1000):
    if (ser.isOpen() == False):
        continue
    data = ser.read(16)
    t = ((ord(data[3]) * 256 + ord(data[2])) * 256 + ord(data[1])) * 256 + ord(data[0])
    ax = read_buf(data, 4) / 4096.0
    ay = read_buf(data, 6) / 4096.0
    az = read_buf(data, 8) / 4096.0
    gx = read_buf(data, 10) / 65.5
    gy = read_buf(data, 12) / 65.5
    gz = read_buf(data, 14) / 65.5

    output = str(t) + ' ' + str(ax) + ' ' + str(ay) + ' ' + str(az) + ' ' + str(gx) + ' ' + str(gy) + ' ' + str(gz)
    print output
    fout.write(output + '\n')

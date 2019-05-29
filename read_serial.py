import serial
import time
import madgwickahrs
import math
import numpy as np

class ReadSerial():
    offset_gx = +0.094
    offset_gy = -0.013
    offset_gz = -0.009

    ser = None
    mad = None
    heading = 0

    def __init__(self):
        self.ser = serial.Serial('COM6', 250000)
        time.sleep(1)
        self.ser.read(self.ser.in_waiting)
        self.mad = madgwickahrs.MadgwickAHRS(0.001)
    
    def read_buf(self, data, offset):
        x = ord(data[offset + 1]) * 256 + ord(data[offset])
        if x >= 32768:
            x -= 65536
        return x

    def get_data(self):
        while (self.mad == None):
            time.sleep(0.1)
        
        data = self.ser.read(17)
        t = ((ord(data[3]) * 256 + ord(data[2])) * 256 + ord(data[1])) * 256 + ord(data[0])
        ax = self.read_buf(data, 4) / 4096.0
        ay = self.read_buf(data, 6) / 4096.0
        az = self.read_buf(data, 8) / 4096.0
        gx = self.read_buf(data, 10) / 65.5 * (math.pi / 180.0) - self.offset_gx
        gy = self.read_buf(data, 12) / 65.5 * (math.pi / 180.0) - self.offset_gy
        gz = self.read_buf(data, 14) / 65.5 * (math.pi / 180.0) - self.offset_gz
        is_touch = ord(data[16])
        self.mad.update_imu([gx, gy, gz], [ax, ay, az])
        [gra_x, gra_y, gra_z] = self.mad.calc_gravity()
        ax -= gra_x
        ay -= gra_y
        az -= gra_z
        gra_x = min(gra_x, +1)
        gra_x = max(gra_x, -1)
        pitch, heading = self.mad.calc_angles()
        self.heading += gz * 0.001
        return [t, gx, gy, gz, ax, ay, az, gra_x, gra_y, gra_z, pitch, self.heading, is_touch]

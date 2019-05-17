import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from IPython import display
import time
import threading

class Oscilloscope:
    data = []

    def __init__(self):
        plt.ion()
        thread = threading.Thread(target = self.draw_data)
        thread.start()

    def draw_data(self):
        plt.figure(figsize=(10, 4))
        
        while self.data != None:
            plt.clf()
            #plt.xlim(-0.5, 0.5)
            plt.ylim(-1.5, 1.5)
            if (self.data != None and len(self.data) > 0):
                length = len(self.data)
                data = np.array(self.data).reshape(length, -1)
                for i in range(np.size(data, 1)):
                    plt.plot(data[:, i])
                #plt.plot(data[:,1], data[:,0])
            plt.pause(0.001)
            time.sleep(0.05)
    
    def append_data(self, frame):
        self.data.append(frame)
        if (len(self.data) > 50):
            self.data.pop(0)    

    def stop(self):
        self.data = None

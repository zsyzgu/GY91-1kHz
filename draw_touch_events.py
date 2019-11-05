import read_serial
import oscilloscope
import keyboard
import panel
import pygame
import entry
import time
import math
import event
import log
import numpy as np
from cv2 import cv2
import threading
import time

length = 50
image = np.zeros((300, 600, 3), np.uint8)
updated = False
running = True
start = time.time()
start2 = time.time()
flag = 0
flag2 = 0
swipe_flag = False

def update():
    cv2.imshow('image', image)
    global updated
    global running
    while running:
        if updated:
            cv2.imshow('image', image)
            updated = False
        cv2.waitKey(5)

thread = threading.Thread(target = update)
thread.start()

def clear():
    cv2.rectangle(image, (0, 0), (600, 150), (0, 0, 0), -1)
    global updated
    updated = True

def clear2():
    cv2.rectangle(image, (0, 150), (600, 300), (0, 0, 0), -1)
    global updated
    updated = True

def text(s):
    cv2.rectangle(image, (0, 0), (600, 150), (0, 0, 0), -1)
    cv2.putText(image, s, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
    global updated
    updated = True
    global start
    start = time.time()
    global flag
    flag = 1

def text2(s):
    cv2.rectangle(image, (0, 150), (600, 300), (0, 0, 0), -1)
    cv2.putText(image, s, (0, 250), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
    global updated
    updated = True
    global start2
    start2 = time.time()
    global flag2
    flag2 = 1

input = read_serial.ReadSerial()
input.get_data()
event = event.Event()

T = 0
while True:
    T += 1
    if T % 10 == 0 and keyboard.is_pressed('q'):
        running = False
        break
    #if T % 100 == 5 and keyboard.is_pressed('s'):
    #    swipe_flag = True
    data = input.get_data()
    curr_event = event.get_event(data)
    if curr_event == event.TOUCH_DOWN:
        text('Touch')
    if T % 100 == 5 and keyboard.is_pressed('s'):
        text('Touch')
    if curr_event == event.TOUCH_UP or curr_event == event.SLIDE_LEFT:
        text2('Touchup')
    #elif curr_event == event.SLIDE_LEFT:
    #    text2('Swipe')
    #    if swipe_flag:
    #        text2('Swipe')
    #        swipe_flag = False
    #if curr_event == event.LONG_PRESS:
    #    text2('Long Press')
    if flag == 1 and time.time() - start >= 0.1:
        clear()
        flag = 0
    if flag2 == 1 and time.time() - start2 >= 0.1:
        clear2()
        flag2 = 0

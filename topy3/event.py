import contact
import touch
import numpy as np
import time

class Event:
    THRESHOLD_touch_down = 5 # duration between touch up judgement and touch down
    THRESHOLD_touch_up = 15 # frames to confirm a touch up event
    THRESHOLD_long_press = 300 # duration between long press and touch down
    THRESHOLD_slide_distance = 0.1

    cont = contact.Contact()
    touchup = touch.TouchUp()
    last_tapping = 0
    up_not_triggered = False
    long_press_not_triggered = False
    count_down = 0
    count_up = 0
    queue_len = 1000
    queue = np.zeros(queue_len)
    queue_tot = 0

    NO_EVENT = -1
    TOUCH_DOWN = 0
    TOUCH_UP = 1
    LONG_PRESS = 2
    SLIDE_LEFT = 3

    time_cnt = 0

    def get_event(self, data):
        timestamp = int(data[0])
        nine_axis = data[1 : 10]
        heading = data[11]
        curr_event = self.NO_EVENT

        self.queue[self.queue_tot % self.queue_len] = heading
        self.queue_tot += 1
        duration = (timestamp - self.last_tapping) / 1000
        is_slide = heading - self.queue[(self.queue_tot - duration) % self.queue_len] > self.THRESHOLD_slide_distance
        
        self.cont.update(nine_axis)
        if (not self.up_not_triggered) and self.cont.is_contact():
            self.last_tapping = timestamp
            self.count_down = self.THRESHOLD_touch_down
            curr_event = self.TOUCH_DOWN
        
        if self.count_down >= 1:
            self.count_down -= 1
            if self.count_down == 0:
                self.up_not_triggered = True
                self.long_press_not_triggered = True
        
        self.touchup.update(data)
        if self.up_not_triggered:
            # detect touch up event with machine learning
            if self.time_cnt == 1 and self.touchup.is_touchup(self.last_tapping):
                curr_event = self.TOUCH_UP
                if is_slide:
                    curr_event = self.SLIDE_LEFT
                self.up_not_triggered = False
                self.long_press_not_triggered = False
            self.time_cnt = 1 - self.time_cnt
            # detect touch up event with rules
            '''
            up = nine_axis[3] * nine_axis[6] + nine_axis[4] * nine_axis[7] + nine_axis[5] * nine_axis[8]
            mo = nine_axis[3] * nine_axis[3] + nine_axis[4] * nine_axis[4] + nine_axis[5] * nine_axis[5]
            if up <= -0.1 and up ** 2 >= mo * 0.5: # The force is enough; The direction is correct
                self.count_up += 1
            else:
                self.count_up = 0
            if (self.count_up >= self.THRESHOLD_touch_up):
                self.count_up = 0
                curr_event = self.TOUCH_UP
                self.up_not_triggered = False
                self.long_press_not_triggered = False
            '''
        if self.long_press_not_triggered and timestamp - self.last_tapping >= self.THRESHOLD_long_press * 1000:
            if not is_slide:
                curr_event = self.LONG_PRESS
                self.long_press_not_triggered = False
        
        return curr_event

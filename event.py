import contact

class Event:
    cont = contact.Contact()
    last_movement = 0
    last_tapping = 0
    long_event_not_triggered = False
    total_acc_2 = 0

    def get_event(self, data):
        timestamp = data[0]
        nine_axis = data[1 : 10]

        event_touch_down = False
        event_long_press = False
        event_long_idle = False

        acc_2 = nine_axis[3] ** 2 + nine_axis[4] ** 2 + nine_axis[5] ** 2
        if acc_2 >= 0.15 ** 2:
            self.last_movement = timestamp
            self.long_event_not_triggered = True
        
        if self.cont.update(nine_axis):
            event_touch_down = True
            self.last_tapping = timestamp
            self.total_acc_2 = 0
        elif timestamp >= self.last_tapping + 80 * 1000:
            self.total_acc_2 += acc_2
        
        if self.long_event_not_triggered:
            if timestamp - self.last_movement > 150 * 1000 and self.last_movement - self.last_tapping < 80 * 1000: # Long Press (200 ms)
                if self.total_acc_2 <= 1:
                    event_long_press = True
                self.long_event_not_triggered = False
            elif timestamp - self.last_movement > 300 * 1000 and self.last_movement - self.last_tapping >= 80 * 1000: # Long Idle (400 ms)
                event_long_idle = True
                self.long_event_not_triggered = False
        
        return event_touch_down, event_long_press, event_long_idle

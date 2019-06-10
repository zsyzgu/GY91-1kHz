import contact

class Event:
    cont = contact.Contact()
    last_movement = 0
    last_tapping = 0
    long_event_not_triggered = False

    def get_event(self, timestamp, nine_axis):
        event_touch_down = False
        event_long_press = False
        event_long_idle = False

        if nine_axis[3] ** 2 + nine_axis[4] ** 2 + nine_axis[5] ** 2 >= 0.2 ** 2:
            self.last_movement = timestamp
            self.long_event_not_triggered = True
        
        if self.cont.update(nine_axis):
            event_touch_down = True
            self.last_tapping = timestamp
        
        if self.long_event_not_triggered and timestamp - self.last_movement > 400 * 1000:
            self.long_event_not_triggered = False
            if self.last_movement - self.last_tapping < 80 * 1000:
                event_long_press = True
            else:
                event_long_idle = True
        
        return event_touch_down, event_long_press, event_long_idle

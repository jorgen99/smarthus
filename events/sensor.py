class Sensor:
    def __init__(self, house, unit):
        self.house = house
        self.unit = unit

    def event_is_from_me(self, event):
        return self.house == event.house and self.unit == event.unit
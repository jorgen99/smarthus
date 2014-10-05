from events.constants import Constants


class Event:
    def __init__(self, data):
        data_dict = Event.__create_data_dict(data)
        self.id = data_dict.get("id", None)
        self.protocol = data_dict.get("protocol", None)
        self.house = data_dict.get("house", None)
        self.unit = data_dict.get("unit", None)
        self.method = data_dict.get("method", None)
        self.group = data_dict.get("group", None)
        self.model = data_dict.get("model", None)
        self.clazz = data_dict.get("class", None)
        self.temp = data_dict.get("temp", None)

    @staticmethod
    def __create_data_dict(data):
        if data.endswith(";"):
            data = data[:-1]
        data_dict = dict(token.split(":") for token in data.split(";"))
        return data_dict

    def is_temperature_event(self):
        return self.temp is not None

    def is_light_event(self):
        return Constants.LIGHT_RELAY.event_is_from_me(self)

    def is_motion_event(self):
        return Constants.MOVEMENT_SENSOR.event_is_from_me(self)

    def is_command(self):
        return self.clazz is not None

    def should_be_handled(self):
        return self.protocol in Constants.VALID_PROTOCOLS

    def is_turn_on(self):
        return self.method == Constants.ON

    def is_turn_off(self):
        return self.method == Constants.OFF

    def it_became_dark(self):
        return self.is_light_event() and self.is_turn_on()

    def it_became_light(self):
        return self.is_light_event() and self.is_turn_off()

    def motion_activated(self):
        return self.is_motion_event() and self.is_turn_on()

    def no_motion_for_a_while(self):
        return self.is_motion_event() and self.is_turn_off()

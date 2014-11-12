# coding=utf-8
from tellcore import constants as const
import time
from events.constants import Constants
import datetime


class EventHandler:
    def __init__(self, device_locator, event):
        self.device_locator = device_locator
        self.event = event

    def handle_event(self):
        if self.event.it_became_dark():
            self.__control_lights(Constants.MOOD_LIGHTS, Constants.ON)
        elif self.event.it_became_light():
            self.__control_lights(Constants.MOOD_LIGHTS, Constants.OFF)
        elif self.event.motion_activated():
            self.__control_lights(Constants.MOTION_CONTROLLED_LGHTS, Constants.ON)
        elif self.event.no_motion_for_a_while():
            self.__control_lights(Constants.MOTION_CONTROLLED_LGHTS, Constants.OFF)

    def __control_lights(self, light_ids, light_command):
        for device_id in light_ids:
            device = self.device_locator.find_device(device_id)
            if device is not None:
                self.__send_command_to_device(light_command, device)

    def __send_command_to_device(self, command, device):
        cmd = self.__last_command(device)

        timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        if (command == Constants.OFF and
                (cmd == const.TELLSTICK_TURNON or cmd == const.TELLSTICK_DIM)):
            encoded_name = self.__encode(device.name)
            print("{} : Av - {}".format(timestamp, encoded_name))
            for _ in [1, 2, 3]:
                device.turn_off()
                self.__status_and_sleep(device)
        elif command == Constants.ON and cmd == const.TELLSTICK_TURNOFF:
            encoded_name = self.__encode(device.name)
            on = self.__encode("På")
            print("{} : {} - {}".format(timestamp, on, encoded_name))
            for _ in [1, 2, 3]:
                if device.id == 2:
                    device.dim(Constants.DIM_LEVEL)
                else:
                    device.turn_on()
                self.__status_and_sleep(device)

    def __status_and_sleep(self, device):
        self.__last_command(device)
        time.sleep(0.5)

    @staticmethod
    def __last_command(device):
        return device.last_sent_command(
            const.TELLSTICK_TURNON
            | const.TELLSTICK_TURNOFF
            | const.TELLSTICK_DIM)

    @staticmethod
    def __encode(x):
        """ Do not die on bad input when doing debug prints """
        if type(x) == str:
            return x
        else:
            return x.encode("utf-8")


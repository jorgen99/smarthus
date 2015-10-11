# coding=utf-8
from tellcore import constants as const
import time
from events.constants import Constants
from events.status import Status
from datetime import datetime


class EventHandler:
    def __init__(self, device_locator, status):
        print('skapar event handler')
        self.device_locator = device_locator
        self.status = status
        

    def handle(self, event):
        if event.it_became_dark():
            self.status.turn_on()
            self.__control_lights(Constants.MOOD_LIGHTS, Constants.ON)
        elif event.it_became_light():
            self.status.turn_off()
            self.__control_lights(Constants.MOOD_LIGHTS, Constants.OFF)
        elif self.time_to_turn_out_lights():
            print('slacker allt')
            self.status.turn_off()
            for device in self.device_locator.all():
                self.__send_command_to_device(Constants.OFF, device)
        elif event.motion_activated():
            self.__control_lights(Constants.MOTION_CONTROLLED_LGHTS, Constants.ON)
        elif event.no_motion_for_a_while():
            self.__control_lights(Constants.MOTION_CONTROLLED_LGHTS, Constants.OFF)

    def time_to_turn_out_lights(self):
        d = datetime.now()
        print("{0}:{1} - {2}".format(d.hour, d.minute, self.status.is_turned_on()))
        if (d.hour == 23 and d.minute < 3) and self.status.is_turned_on():
            print('japp, ska slacka')
            return True
        else:
            print('nae, ska inte slacka')
            return False

    def __control_lights(self, light_ids, light_command):
        for device_id in light_ids:
            device = self.device_locator.find_device(device_id)
            if device is not None:
                self.__send_command_to_device(light_command, device)

    def __send_command_to_device(self, command, device):
        cmd = self.__last_command(device)

        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
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


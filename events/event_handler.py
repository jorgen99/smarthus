# coding=utf-8

import time
from datetime import datetime
from tellcore import constants as const
from events.constants import Constants
from events.greenhouse import add_temperature


class EventHandler:
    def __init__(self, device_locator, status):
        self.device_locator = device_locator
        self.status = status

    def handle(self, event):
        if event.it_became_dark():
            self.debug_print("Det blev morkt")
            self.status.turn_on()
            self.__control_lights(Constants.MOOD_LIGHTS, Constants.ON)
            self.__control_lights(Constants.NIGHT_LIGHTS, Constants.ON)

        elif event.it_became_light():
            self.debug_print("Det blev ljust")
            self.status.turn_off()
            self.__control_lights(Constants.MOOD_LIGHTS, Constants.OFF)
            self.__control_lights(Constants.NIGHT_LIGHTS, Constants.OFF)

        elif self.time_to_turn_out_lights():
            self.debug_print("Dags att slacka for natten")
            self.__turn_off_all_but_night_lights()

        elif event.motion_activated():
            self.debug_print("Rorelsedackare aktiverad")
            self.__control_lights(Constants.MOTION_CONTROLLED_LGHTS, Constants.ON)
        elif event.no_motion_for_a_while():
            self.debug_print("Ingen rorelse på ett tag")
            self.__control_lights(Constants.MOTION_CONTROLLED_LGHTS, Constants.OFF)

        elif event.morning_on():
            self.debug_print("Någon tryckte PÅ lampknappen")
            self.__control_lights(Constants.MORNING_LIGHTS, Constants.ON)
        elif event.morning_off():
            self.debug_print("Någon tryckte AV lampknappen")
            self.__turn_off_all_but_night_lights()

        elif event.is_temperature_humidity_event():
            msg = "temperature;{0};humidity;{1}".format(event.temp, event.humidity)
            # self.debug_print(msg)
            event_string = event.to_string()
            self.debug_print(event_string)

            now = datetime.now()
            file_msg = "date;{0};{1}".format(now.isoformat(), msg)
            # with open('/var/log/smarthus.log', 'a') as the_file:
            #     the_file.write(file_msg + "\n")

            # with open('allt.log', 'a') as allt_file:
            #     line = "{0} - {1}\n".format(now.isoformat(), event_string)
            #     allt_file.write(line)

            if event.id == "183" and now.minute in [0, 1, 29, 30, 31, 59]:
                self.debug_print("Yo, 183!")
                with open('greenhouse_log.txt', 'a') as the_file:
                    the_file.write(file_msg + "\n")
                add_temperature((now.isoformat(), float(event.temp)))

    @staticmethod
    def debug_print(msg):
        now = datetime.now()
        print("{0} - {1}".format(now.isoformat(), msg))

    def time_to_turn_out_lights(self):
        d = datetime.now()
        if (d.hour == 23 and d.minute < 3) and self.status.is_turned_on():
            print('japp, ska slacka')
            return True
        else:
            return False

    def __turn_off_all_but_night_lights(self):
        print('slacker allt utom natt lampor')
        self.status.turn_off()
        for device in self.device_locator.all():
            encoded_name = self.__encode(device.name)
            self.debug_print("Kanske släcka: {0}".format(encoded_name))
            if device.id in Constants.NIGHT_LIGHTS:
                self.debug_print("Slacker inte nattljus: {0}".format(encoded_name))
                continue
            else:
                self.debug_print("Ja släcker {0}".format(encoded_name))
                self.__send_command_to_device(Constants.OFF, device)

    def __control_lights(self, light_ids, light_command):
        for device_id in light_ids:
            device = self.device_locator.find_device(device_id)
            if device is not None:
                self.__send_command_to_device(light_command, device)
            else:
                print("Light with id {0} was None!".format(device_id))

    def __send_command_to_device(self, command, device):
        last_command = self.__last_command(device)
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        encoded_name = self.__encode(device.name)
        print("Sending command {0} to device {1}".format(command, encoded_name))

        if (command == Constants.OFF and
                (last_command == const.TELLSTICK_TURNON or last_command == const.TELLSTICK_DIM)):
            encoded_name = self.__encode(device.name)
            print("   {} : Av - {}".format(timestamp, encoded_name))
            for _ in [1, 2, 3]:
                device.turn_off()
                self.__status_and_sleep(device)
        elif command == Constants.ON and last_command == const.TELLSTICK_TURNOFF:
            on = self.__encode("På")
            print("   {} : {} - {}".format(timestamp, on, encoded_name))
            for _ in [1, 2, 3]:
                if device.id == 2:
                    device.dim(Constants.DIM_LEVEL)
                else:
                    device.turn_on()
                self.__status_and_sleep(device)
        else:
            msg = "   Inte av och inte på... command: {}, last_command: {}"
            print(msg.format(command, last_command))

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

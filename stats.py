# coding=utf-8

import tellcore.telldus as td
import tellcore.constants as const
from daemon.device_locator import DeviceLocator


core = td.TelldusCore()

if __name__ == '__main__':
    device_locator = DeviceLocator(core)
    device_ids = [1, 2, 3, 4, 5, 6, 7]
    for id in device_ids:
        device = device_locator.find_device(id)



# coding=utf-8

import tellcore.telldus as td
import tellcore.constants as const


def find_device(device, devices):
    for d in devices:
        if str(d.id) == device or d.name == device:
            return d
    print("Device '{}' not found".format(device))
    return None

core = td.TelldusCore()

device = find_device("1", core.devices())
print(device.name)
print(device.last_sent_command(4095))

print
for d in core.devices():
    dimable = d.methods(255) & const.TELLSTICK_DIM == const.TELLSTICK_DIM
    print(u"{} {} {}".format(d.id, d.name, dimable))

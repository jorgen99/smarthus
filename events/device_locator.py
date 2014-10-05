# coding=utf-8
class DeviceLocator:

    def __init__(self, core):
        self.core = core
        self.devices = {}

    def find_device(self, device_id):
        device = self.devices.get(device_id)
        if device is None:
            device = self.__find(device_id)
            self.devices[device_id] = device

        return device

    def __find(self, device_id):
        for device in self.core.devices():
            if device.id == device_id:
                return device
        return None

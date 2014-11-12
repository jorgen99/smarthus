# coding=utf-8
class DeviceLocator:

    def __init__(self, core):
        self.core = core
        self.device_cache = {}

    def find_device(self, device_id):
        device = self.device_cache.get(device_id)
        if device is None:
            device = self.__find(device_id)
            self.device_cache[device_id] = device

        return device

    def __find(self, device_id):
        for device in self.core.devices():
            if device.id == device_id:
                return device
        return None

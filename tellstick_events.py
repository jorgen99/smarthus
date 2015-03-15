# coding=utf-8

import tellcore.telldus as td

from events.device_locator import DeviceLocator
from events.event import Event
from events.event_handler import EventHandler


def raw_event(data, controller_id, cid):
    event = Event(data)
    EventHandler(device_locator, event).handle_event()


try:
    import asyncio

    loop = asyncio.get_event_loop()
    dispatcher = td.AsyncioCallbackDispatcher(loop)
except ImportError:
    loop = None
    dispatcher = td.QueuedCallbackDispatcher()

core = td.TelldusCore(callback_dispatcher=dispatcher)
device_locator = DeviceLocator(core)
core.register_raw_device_event(raw_event)

try:
    if loop:
        loop.run_forever()
    else:
        import time

        while True:
            core.callback_dispatcher.process_pending_callbacks()
            time.sleep(0.5)
except KeyboardInterrupt:
    pass

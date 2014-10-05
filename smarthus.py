# coding=utf-8
from flask import Flask
from flask.templating import render_template

import tellcore.telldus as td
import tellcore.constants as const

import json

app = Flask(__name__)
core = td.TelldusCore()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/devices')
def devices_json():
    return device_info()


@app.route('/devices/turnOffAll', methods = ['POST'])
def turnOffAll():
    for device in core.devices():
        device.turn_off()
    return device_info()

@app.route('/devices/toggle/<int:device_id>', methods = ['POST'])
def toggle(device_id):
    device = find_device(device_id)
    if command(device) == "success":
        device.turn_off()
    else:
        if device.id == 2:
            device.dim(80)
        else:
            device.turn_on()
    return json.dumps(device_tupl(device))


def device_info():
    devices = []
    for device in core.devices():
        devices.append(device_tupl(device))
    return json.dumps(devices)


def device_tupl(device):
    status = command(device)
    return {
        'id': device.id,
        'name': device.name,
        'status': status,
        'label': label(status)
    }


def find_device(device_id):
    for d in core.devices():
        if str(d.id) == str(device_id):
            return d
    print("Device '{}' not found".format(device_id))
    return None


def command(device):
    cmd = device.last_sent_command(
        const.TELLSTICK_TURNON
        | const.TELLSTICK_TURNOFF
        | const.TELLSTICK_DIM)
    if cmd == const.TELLSTICK_TURNON:
        cmd_str = "success"
    elif cmd == const.TELLSTICK_TURNOFF:
        cmd_str = "danger"
    elif cmd == const.TELLSTICK_DIM:
        #cmd_str = "DIMMED:{}".format(device.last_sent_value())
        cmd_str = "success"
    else:
        cmd_str = "UNKNOWN:{}".format(cmd)
    return cmd_str


def label(status):
    if status == "danger":
        return "Sätt på"
    else:
        return "Stäng av"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

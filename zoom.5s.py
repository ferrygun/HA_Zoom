#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
# -*- coding: utf-8 -*-
# <xbar.title>Zoom (Python)</xbar.title>
# <xbar.version>v1.0.0</xbar.version>
# <xbar.author>Ferry Djaja</xbar.author>
# <xbar.author.github>fdjaja</xbar.author.github>
# <xbar.desc>Show Zoom Status</xbar.desc>
# <xbar.image>http://i.imgur.com/P6aNey5.png</xbar.image>
# <xbar.dependencies>python</xbar.dependencies>


import sys
import random
import subprocess
import time
import os
import struct

import paho.mqtt.client as mqtt

# mosquitto_pub -h x.x.x.x -t home/livingroom/zoom -m 0

broker = ''
port = 1883
topic = 'home/livingroom/zoom'
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = ''
password = ''


def zoom_status():
    p1 = subprocess.Popen(["ps", "x"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "-E", "\-key [0-9]"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()

    output = p2.communicate()[0]
    if output:
        code = output.split()[-1].decode()
        code = "ON"
    else:
        code = "OFF"

    return code


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def run():
    time.sleep(1)
    msg = zoom_status()

    print(msg)
 
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port, 60)

    result = client.publish(topic, payload=msg, qos=0, retain=False)
    status = result[0]


if __name__ == '__main__':
    run()

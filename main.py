#!/usr/bin/python3
"""
Blinkt! LED Raspberry Pi MQTT Client firmware

before use:
  sudo apt-get install mosquitto-clients
  pip3 install -r requirements.txt

"""
import time
import random
import threading
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import blinkt
from effects import binary_clock, binary_clock_meld, rainbow, tetris, larson, larson_hue, candle, pulse


broker = '10.10.10.11'
state_topic = 'zero_w/light/state'
command_topic = 'zero_w/light/command'
availability_topic = 'zero_w/status'
blinkt.clear_on_exit = True

def none(*args, **kwargs):
    pass

class BlinktLED:
    effect_dict = {'None': none,
                   'Binary Clock': binary_clock.BinaryClock,
                   'Binary Clock Meld': binary_clock_meld.BinaryClockMeld,
                   'Candle': candle.Candle,
                   'Larson': larson.Larson,
                   'Larson Hue': larson_hue.LarsonHue,
                   'Pulse': pulse.Pulse,
                   'Rainbow': rainbow.Rainbow,
                   'Tetris': tetris.Tetris,
                  }

    def __init__(self):
        blinkt.clear()
        blinkt.show()

        self.state = 'OFF'
        self.brightness = 1
        self.rgb_color = (255, 255, 255)
        self.effect = 'None'
        self.effect_speed = 50

        self.effect_thread = None
        self.publish_state()

    def set_state(self, json_value):
        if json_value['state'] == 'OFF':
            self.state = 'OFF'
        elif json_value['state'] == 'ON':
            self.state = 'ON'
        if json_value.get('brightness'):
            self.brightness = json_value['brightness'] /255
        if json_value.get('color'):
            self.rgb_color = (json_value['color']['r'], json_value['color']['g'], json_value['color']['b'])
        if json_value.get('effect'):
            self.effect = json_value['effect']

    def show(self):
        print(self.__dict__)
        if self.effect_thread:
            self.effect_thread.running = False
            self.effect_thread.thread.join()
            self.effect_thread = None

        if self.state == 'OFF':
            blinkt.clear()
            blinkt.show()
            self.publish_state()

        elif self.effect == 'None':
            blinkt.set_all(*self.rgb_color, brightness=self.brightness)
            blinkt.show()
            self.publish_state()

        else:
            if self.effect in self.effect_dict.keys():
                self.publish_state()
                self.effect_thread = self.effect_dict[self.effect](brightness=self.brightness, rgb_color=self.rgb_color)

    def publish_state(self):
        state = self.__dict__.copy()
        del state['effect_thread']
        state['brightness'] = state['brightness'] *255
        client.publish(state_topic, str(json.dumps(state)))


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(command_topic)
    client.publish(availability_topic, 'online')

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(payload)
    json_value = json.loads(payload)
    led.set_state(json_value)
    led.show()

if __name__=='__main__':
    client = mqtt.Client()
    client.connect(broker,1883,60)

    client.on_connect = on_connect
    client.on_message = on_message

    led = BlinktLED()

    client.loop_forever()

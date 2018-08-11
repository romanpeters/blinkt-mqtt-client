# blinkt-mqtt-client
Raspberry Pi Blinkt! LED MQTT Client

## Features:
- Control the color and brightness of your [Blinkt!](https://shop.pimoroni.com/products/blinkt) LED.
- Integrates well with Home Assistant.
- Effects with variable brightness and color based on the effects from https://github.com/pimoroni/blinkt.

## Installation:
1. Install MQTT client software  
`$ sudo apt-get install mosquitto-clients`  
1. Install Python dependencies  
`$ pip3 install -r requirements.txt`  
1. Run it  
`$ python3 main.py`  
1. See `lights.yaml` on https://github.com/romanpeters/home-assistant for Home Assistant integration.

## Auto-start
1. Create a systemd unit file
`$ sudo nano /lib/systemd/system/blinkt.service`  
with the following contents: 

```
[Unit]
Description=blinkt
After=network.target

[Service]
Type=simple
User=your username
WorkingDirectory=/path/to/blinkt-mqtt-client
ExecStart=/usr/local/bin/python3 /path/to/blinkt-mqtt-client/main.py

[Install]
WantedBy=multi-user.target
```  
Fill in your username, path to the files and Python executable where necessary.  
2. Update systemd  
`$ sudo systemctl daemon-reload`  
3. Enable auto-start on boot
`$ sudo systemctl enable blinkt.service`

# About

*stroll* is a simple script to get data from Raspberry Pi sensors and publish to a MQTT broker.

## Purpose

Get data from Raspberry Pi sensors and push to MQTT broker :
* get data from Raspberry Pi sensors
* push data to MQTT broker
* run as service
* handle the absence or the rewiring of sensors gracefully
* "smart" / eco polling : poll often when data changes, less often when constant
* (optional) include some system metrics (cpu, ram, disk usage)
* (optional) push to other destination than MQTT

## Status

Currently a very basic proof of concept. Works with manual steps and no frills.


# Installing

## Dependencies

This project depends on :
* the [paho-mqtt](https://github.com/eclipse/paho.mqtt.python) library for connecting to a MQTT broker
* the [Adafruit-DHT](https://github.com/adafruit/Adafruit_Python_DHT/) library for querying the DHT11 sensor
Import the Python dependencies :
In your virtual environment folder, do :
```sh
python -m pip install -r ./lib/stroll/requirements.txt
```

## Deploying

Can be run as a simple python script with :
```sh
python .lib/stroll/stroll.py
```

Can be run as as a service, and unit file `./sytemd/stroll.service` is provided as an example.

Can be deployed using Ansible, but this should probably be tweaked first to your configuration :
```sh
ansible-playbook ./ansible/install_stroll.yaml
```


# Contributing

This is a very small project authored by a beginner for fun.
Currently I don't have plans for collaboration, but feedback is welcome and of course feel free to fork.

# License

MIT

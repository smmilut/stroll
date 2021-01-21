#!/usr/local/lib/stroll/virtualenv/bin/python3
"""
    Get temperature / humidity data from DHT11 and publish MQTT

    simple implementation to test full workflow on raspberry pi

    requires Adafruit_DHT

    smmilut 2021-01-21
"""
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s in %(module)s(%(name)s) : %(message)s',
    level=logging.DEBUG)
log = logging.getLogger(__name__)

import time
from datetime import datetime, timedelta

import Adafruit_DHT
import paho.mqtt.client as mqtt

class ConnectionDHT:
    def __init__(self, pin, sensor_type=Adafruit_DHT.DHT11):
        """
            initialize connection to device
        """
        self.isConnectionOK = False
        self.sensor_type = sensor_type
        self.pin = pin
        self.retries = 15
        self.retry_delay = 2
        self.sleep_time = 60
        self.humidity = None
        self.temperature = None
        self.ts = None

    def get_data(self):
        """ try to get data """
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor_type, self.pin, retries=self.retries, delay_seconds=self.retry_delay)
        if humidity is not None and temperature is not None:
            self.ts = datetime.now()
            self.humidity = humidity
            self.temperature = temperature
            self.isConnectionOK = True
            log.debug("reading humidity={}% and temperature={}°C".format(humidity, temperature))
        else:
            self.isConnectionOK = False
            log.warning("invalid reading of humidity={} and temperature={}".format(humidity, temperature))

    def poll_loop(self, maxloop=None, callback=lambda t, h: log.info("{}\n{}".format(t, h))):
        """ execute callback until keyboard interrupt Ctrl+C """
        i = 0
        try:
            while True:
                #self.get_data() # required to flush
                self.get_data()
                if self.isConnectionOK:
                    callback(self.temperature, self.humidity)
                i += 1
                if maxloop is not None and i > maxloop:
                    log.info("Reached maximum number of loops")
                    return
                log.debug("sleeping until next polling in {}s".format(self.sleep_time))
                time.sleep(self.sleep_time)
        except KeyboardInterrupt:
            log.warning("KeyboardInterrupt : exiting loop")

    def __str__(self):
        return "ConnectionDHT{} on pin {}".format(self.sensor_type, self.pin)

class MqttHandler:
    """  wrap around MQTT client  """
    def __init__(self, ip="localhost", port=1883, timeout=60, topic_root="test"):
        self.topic_root = topic_root
        self.client = mqtt.Client(clean_session=True)
        self.client.enable_logger(log)
        self.client.connect(ip, port, timeout)

    def publish(self, data, sensor_name):
        topic = "{}/{}".format(self.topic_root, sensor_name)
        payload = str(data)
        log.debug("sending '{}' on topic '{}'".format(payload, topic))
        self.client.publish(topic, payload=payload, qos=0, retain=False)
def main():
    mqtt = MqttHandler(ip="localhost", topic_root="test")
    dht = ConnectionDHT(4)
    def publish_t_h(t, h):
        mqtt.publish(t, "temperature")
        mqtt.publish(h, "humidity")
    dht.poll_loop(callback=publish_t_h)

if(__name__) == '__main__':
    main()


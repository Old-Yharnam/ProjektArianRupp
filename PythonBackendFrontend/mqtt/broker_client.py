""" 
Verwaltet die MQTT-Verbindung und ist die Schnittstelle zum MQTT-Broker.
"""

from paho.mqtt import client as mqtt_client
import config.settings as settings

class MQTTBrokerClient:
    def __init__(self):
        self.client = mqtt_client.Client()
        self.client.username_pw_set(settings.MQTT_BROKER_USERNAME, settings.MQTT_BROKER_PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def connect(self):
        try:
            self.client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT)
            self.client.loop_start()
            print("Mit MQTT-Broker verbunden.")
        except Exception as e:
            print(f"Fehler beim Verbinden mit MQTT-Broker: {e}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Von MQTT-Broker getrennt.")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Erfolgreich mit MQTT-Broker verbunden.")
            client.subscribe(settings.MQTT_TOPIC_SENSOR)
            print(f"Abonniert: {settings.MQTT_TOPIC_SENSOR}")
        else:
            print(f"Verbindungsfehler mit MQTT-Broker: {rc}")

    def on_disconnect(self, client, userdata, rc):
        print("Verbindung zum MQTT-Broker wurde getrennt.")
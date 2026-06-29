""" 
Verwaltet die eingehenden MQTT-Nachrichten und leitet sie an die entsprechenden Funktionen weiter.
"""

from datetime import datetime

import config.settings as settings
from models.sensor_data import SensorData

sensor_messages = []
sensor_events = []

class MQTTMessageHandler:
    def __init__(self, broker_client):
        self.broker_client = broker_client
        self.broker_client.client.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"Nachricht empfangen - Thema: {topic}, Inhalt: {payload}")

        if topic == settings.MQTT_TOPIC_SENSOR:
            self.handle_sensor(payload)
        else:
            print(f"Unbekanntes Thema: {topic}")

    def handle_sensor(self, payload):
        sensor_messages.append(payload)
        sensor_events.append(
            SensorData(
                sensor_id="hw201",
                timestamp=datetime.now().isoformat(timespec="seconds"),
                values={"raw": payload},
            )
        )
        print(f"Sensor-Ereignis gespeichert: {payload}")


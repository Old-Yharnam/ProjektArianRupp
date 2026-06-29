""" 
Repräsentiert EIN Gerät, das in der Lage ist, Daten zu senden und/oder zu empfangen.
Hier wird die Basisklasse für alle spezifischen Gerätetypen definiert, wie z.B. Sensoren, Aktoren, etc.
"""

import mqtt.broker_client as broker_client

class Device:
    def __init__(self, device_id: str, device_type: str):
        self.device_id = device_id
        self.device_type = device_type
        self.status = "offline"
        self.mqtt_client = broker_client.MQTTBrokerClient()
        self.mqtt_client.client.on_connect = self._on_connect
        self.mqtt_client.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.status = "online"
        else:
            self.status = "offline"

    def _on_disconnect(self, client, userdata, rc):
        self.status = "offline"

    def subscribe_to_data(self):
        topic = f"sensor/{self.device_id}/data"
        self.mqtt_client.client.subscribe(topic)
        self.mqtt_client.client.message_callback_add(topic, self._on_mqtt_message)
        print(f"{self.device_id} abonniert Topic: {topic}")

    def _on_mqtt_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        self.receive_data(msg.topic, payload)

    def receive_data(self, topic, payload):
        """Verarbeitet empfangene Daten vom MQTT-Broker."""
        print(f"Empfangen von {topic}: {payload}")
        
    def get_status(self):
        """Gibt den aktuellen Status des Geräts zurück.""" 
        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "status": self.status
        }
            
class Sensor(Device):
    def __init__(self, device_id: str, sensor_type: str):
        super().__init__(device_id, "Sensor")
        self.sensor_type = sensor_type

    def receive_data(self, topic, payload):
        """Sensoren empfangen normalerweise keine Daten, daher könnte diese Methode leer bleiben oder eine Fehlermeldung ausgeben."""
        print(f"Sensor {self.device_id} ignoriert eingehende Daten von {topic}: {payload}")
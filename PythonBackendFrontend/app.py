"""
Hier ist die Hauptdatei des Projektes, hier wird alles initialisiert, verbunden und gestartet.
Es sollte so wenig wie möglich Code enthalten, damit es übersichtlich bleibt.
Die "if __name__ == '__main__':" befindet sich hier.
"""

from mqtt.broker_client import MQTTBrokerClient
from mqtt.message_handler import MQTTMessageHandler
from mqtt.topic_manager import MQTTTopicManager
from devices.device_registry import DeviceRegistry
from devices.device import Device
from ui.dashboard import Dashboard
from nicegui import ui

def main():
    # Initialisiere zentrale Komponenten
    broker_client = MQTTBrokerClient()
    broker_client.connect()

    topic_manager = MQTTTopicManager()
    device_registry = DeviceRegistry()
    device_registry.add_device(Device("hw201", "Sensor"))
    message_handler = MQTTMessageHandler(broker_client)

    # Beispiel: Dashboard anzeigen
    @ui.page('/')
    def show_dashboard():
        Dashboard.display_dashboard(device_registry=device_registry, topic_manager=topic_manager)
        # Hier könntest du weitere Dashboard-Elemente anzeigen lassen,
        # z.B. device_registry.all_devices() oder Netzwerkstatus

    # Starte das UI
    ui.run()

if __name__ in {'__main__', '__mp_main__'}:
    main()